import streamlit as st
import plotly.express as px
import pandas as pd
import os

from io import BytesIO
from utils.page_header import show_page_header
from utils.pdf_report import generate_pdf_report
from utils.helper import get_revenue_column, get_staff_column
from utils.insight import generate_insights

    
def show_dashboard():

    show_page_header(
        "📊",
        "Dashboard",
        "Ringkasan KPI dan performa penjualan."
    )

    if st.session_state.clean_data is None:
        st.info("Upload dan cleaning data terlebih dahulu.")
        return

    df = st.session_state.clean_data.copy()

    revenue_col = get_revenue_column(df)
    staff_col = get_staff_column(df)

    if revenue_col is None:
        st.error("Kolom revenue tidak ditemukan.")
        return

    # =========================
    # FILTER DASHBOARD
    # =========================
    st.sidebar.subheader("Filter Dashboard")

    # Hapus tanggal kosong
    if "Tanggal_Hari" in df.columns:
        tanggal_min = df["Tanggal_Hari"].min()
        tanggal_max = df["Tanggal_Hari"].max()

        tanggal_filter = st.sidebar.date_input(
            "Pilih Rentang Tanggal",
            value=(tanggal_min, tanggal_max),
            min_value=tanggal_min,
            max_value=tanggal_max
        )

    if len(tanggal_filter) == 2:
        start_date, end_date = tanggal_filter
        df = df[
            (df["Tanggal_Hari"] >= start_date) &
            (df["Tanggal_Hari"] <= end_date)
        ]

        if len(tanggal_filter) == 2:
            start_date, end_date = tanggal_filter
            df = df[
                (df["Tanggal_Hari"] >= start_date) &
                (df["Tanggal_Hari"] <= end_date)
            ]

    if staff_col:
        staff_list = sorted(df[staff_col].dropna().unique())
        selected_staff = st.sidebar.multiselect(
            f"Pilih {staff_col}",
            staff_list,
            default=staff_list
        )
        df = df[df[staff_col].isin(selected_staff)]

    if "Kategori" in df.columns:
        kategori_list = sorted(df["Kategori"].dropna().unique())
        selected_kategori = st.sidebar.multiselect(
            "Pilih Kategori",
            kategori_list,
            default=kategori_list
        )
        df = df[df["Kategori"].isin(selected_kategori)]

    if "Metode Pembayaran" in df.columns:
        payment_list = sorted(df["Metode Pembayaran"].dropna().unique())
        selected_payment = st.sidebar.multiselect(
            "Pilih Metode Pembayaran",
            payment_list,
            default=payment_list
        )
        df = df[df["Metode Pembayaran"].isin(selected_payment)]


    # =========================
    # FILTER SUMMARY
    # =========================
    st.subheader("🔎 Ringkasan Filter")

    filter_col1, filter_col2, filter_col3 = st.columns(3)

    if "Tanggal_Hari" in df.columns:
        filter_col1.info(
            f"""
            **Periode Data**  
            {df["Tanggal_Hari"].min()} s/d {df["Tanggal_Hari"].max()}
            """
        )

    if staff_col and staff_col in df.columns:
        filter_col2.info(
            f"""
            **Jumlah {staff_col}**  
            {df[staff_col].nunique()} orang
            """
        )

    if "Kategori" in df.columns:
        filter_col3.info(
            f"""
            **Jumlah Kategori**  
            {df["Kategori"].nunique()} kategori
            """
        )

    # =========================
    # KPI
    # =========================
    total_revenue = df[revenue_col].sum()
    total_transaksi = df["Nomor"].nunique() if "Nomor" in df.columns else len(df)
    total_qty = df["Qty"].sum() if "Qty" in df.columns else 0
    rata_transaksi = total_revenue / total_transaksi if total_transaksi > 0 else 0

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("💰 Total Revenue", f"Rp {total_revenue:,.0f}")
    col2.metric("🧾 Total Transaksi", f"{total_transaksi:,.0f}")
    col3.metric("☕ Item Terjual", f"{total_qty:,.0f}")
    col4.metric("📈 Average Order", f"Rp {rata_transaksi:,.0f}")

    st.subheader("📌 Executive Summary")

    summary_col1, summary_col2, summary_col3 = st.columns(3)

    if "Item" in df.columns and "Qty" in df.columns:
        top_product = (
            df.groupby("Item", as_index=False)["Qty"]
            .sum()
            .sort_values("Qty", ascending=False)
            .iloc[0]
        )

        summary_col1.info(
            f"""
            **Produk Terlaris**  
            {top_product['Item']}  
            {top_product['Qty']:,.0f} item
            """
        )

    if "Kategori" in df.columns:
        top_category = (
            df.groupby("Kategori", as_index=False)[revenue_col]
            .sum()
            .sort_values(revenue_col, ascending=False)
            .iloc[0]
        )

        summary_col2.success(
            f"""
            **Kategori Terbaik**  
            {top_category['Kategori']}  
            Rp {top_category[revenue_col]:,.0f}
            """
        )

    if "Jam" in df.columns:
        peak_hour = (
            df.groupby("Jam", as_index=False)[revenue_col]
            .sum()
            .sort_values(revenue_col, ascending=False)
            .iloc[0]
        )

        summary_col3.warning(
            f"""
            **Jam Tersibuk**  
            {int(peak_hour['Jam'])}:00  
            Rp {peak_hour[revenue_col]:,.0f}
            """
        )
    
    st.info(
        "Dashboard ini menampilkan performa penjualan Toleransi Kopi "
        "berdasarkan data transaksi yang telah diunggah dan dibersihkan."
    )
    
    # =========================
    # CHART ROW 1
    # =========================
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Revenue Harian")

        if "Tanggal_Hari" in df.columns:
            sales_daily = (
                df.groupby("Tanggal_Hari", as_index=False)[revenue_col]
                .sum()
            )

            fig_daily = px.line(
                sales_daily,
                x="Tanggal_Hari",
                y=revenue_col,
                markers=True,
                title="Tren Revenue Harian"
            )

            st.plotly_chart(
                fig_daily,
                width="stretch"
            )

    with col_right:
        st.subheader("Top 10 Produk Terlaris")

        if "Item" in df.columns and "Qty" in df.columns:
            top_items = (
                df.groupby("Item", as_index=False)["Qty"]
                .sum()
                .sort_values("Qty", ascending=False)
                .head(10)
            )

            fig_items = px.bar(
                top_items,
                x="Qty",
                y="Item",
                orientation="h",
                title="Produk Berdasarkan Qty"
            )

            st.plotly_chart(
                fig_items,
                width="stretch"
            )

    # =========================
    # CHART ROW 2
    # =========================
    col_left2, col_right2 = st.columns(2)

    with col_left2:
        st.subheader("Revenue by Category")

        if "Kategori" in df.columns:
            revenue_category = (
                df.groupby("Kategori", as_index=False)[revenue_col]
                .sum()
                .sort_values(revenue_col, ascending=False)
            )

            fig_category = px.bar(
                revenue_category,
                x="Kategori",
                y=revenue_col,
                title="Revenue Berdasarkan Kategori"
            )

            st.plotly_chart(
                fig_category,
                width="stretch"
            )

    with col_right2:
        st.subheader("Payment Method")

        if "Metode Pembayaran" in df.columns:
            payment_sales = (
                df.groupby("Metode Pembayaran", as_index=False)[revenue_col]
                .sum()
                .sort_values(revenue_col, ascending=False)
            )

            fig_payment = px.pie(
                payment_sales,
                names="Metode Pembayaran",
                values=revenue_col,
                title="Revenue Berdasarkan Metode Pembayaran"
            )

            st.plotly_chart(
                fig_payment,
                width="stretch"
            )

    # =========================
    # CHART ROW 3
    # =========================
    col_left3, col_right3 = st.columns(2)

    with col_left3:
        st.subheader("Revenue by Hour")

        if "Jam" in df.columns:
            revenue_hour = (
                df.groupby("Jam", as_index=False)[revenue_col]
                .sum()
                .sort_values("Jam")
            )

            fig_hour = px.bar(
                revenue_hour,
                x="Jam",
                y=revenue_col,
                title="Revenue Berdasarkan Jam Transaksi"
            )

            st.plotly_chart(
                fig_hour,
                width="stretch"
            )

    with col_right3:
        st.subheader(f"Revenue by {staff_col}")

        if staff_col:
            staff_sales = (
                df.groupby(staff_col, as_index=False)[revenue_col]
                .sum()
                .sort_values(revenue_col, ascending=False)
            )

            fig_staff = px.bar(
                staff_sales,
                x=staff_col,
                y=revenue_col,
                title=f"Revenue Berdasarkan {staff_col}"
            )

            st.plotly_chart(
                fig_staff,
                width="stretch"
            )

    # =========================
    # INSIGHT
    # =========================
    st.divider()
    st.subheader("📌 Insight Otomatis")

    insights = generate_insights(
        df=df,
        revenue_col=revenue_col,
        staff_col=staff_col
    )

    for insight in insights:
        st.success(f"✅ {insight}")

    if "Item" in df.columns and "Qty" in df.columns:
        top_items_insight = (
            df.groupby("Item", as_index=False)["Qty"]
            .sum()
            .sort_values("Qty", ascending=False)
        )

        st.success(
            f"Produk terlaris adalah **{top_items_insight.iloc[0]['Item']}** "
            f"dengan total **{top_items_insight.iloc[0]['Qty']:,.0f} item**."
        )

    if "Kategori" in df.columns:
        category_insight = (
            df.groupby("Kategori", as_index=False)[revenue_col]
            .sum()
            .sort_values(revenue_col, ascending=False)
        )

        st.info(
            f"Kategori dengan revenue tertinggi adalah **{category_insight.iloc[0]['Kategori']}** "
            f"sebesar **Rp {category_insight.iloc[0][revenue_col]:,.0f}**."
        )

    if "Metode Pembayaran" in df.columns:
        payment_insight = (
            df.groupby("Metode Pembayaran", as_index=False)[revenue_col]
            .sum()
            .sort_values(revenue_col, ascending=False)
        )

        st.warning(
            f"Metode pembayaran paling dominan adalah **{payment_insight.iloc[0]['Metode Pembayaran']}** "
            f"dengan revenue **Rp {payment_insight.iloc[0][revenue_col]:,.0f}**."
        )

    if "Jam" in df.columns:
        hour_insight = (
            df.groupby("Jam", as_index=False)[revenue_col]
            .sum()
            .sort_values(revenue_col, ascending=False)
        )

        st.success(
            f"Jam dengan revenue tertinggi adalah pukul **{int(hour_insight.iloc[0]['Jam'])}:00** "
            f"dengan revenue **Rp {hour_insight.iloc[0][revenue_col]:,.0f}**."
        )
    
    
        st.divider()
        st.subheader("📄 Export Report")

        chart_images = []

        def add_chart_to_pdf(title, fig):
            try:
                fig.update_layout(
                    template="plotly_white",
                    width=900,
                    height=500,
                    font=dict(size=14),
                    title=dict(
                        text=title,
                        font=dict(size=22),
                        x=0.5
                    ),
                    margin=dict(l=60, r=40, t=80, b=80)
                )

                for trace in fig.data:
                    if trace.type == "scatter":
                        trace.line.color = "#1E5FD8"
                        trace.marker.color = "#1E5FD8"

                    elif trace.type == "bar":
                        trace.marker.color = "#1E5FD8"

                img_buffer = BytesIO()
                fig.write_image(
                    img_buffer,
                    format="png",
                    scale=2
                )
                img_buffer.seek(0)

                chart_images.append((title, img_buffer))

            except Exception as e:
                st.warning(f"Grafik '{title}' gagal dimasukkan ke PDF: {e}")

        if "Tanggal_Hari" in df.columns:
            sales_daily_pdf = (
                df.groupby("Tanggal_Hari", as_index=False)[revenue_col]
                .sum()
            )

            fig_daily_pdf = px.line(
                sales_daily_pdf,
                x="Tanggal_Hari",
                y=revenue_col,
                markers=True,
                title="Tren Revenue Harian"
            )

            add_chart_to_pdf("Tren Revenue Harian", fig_daily_pdf)

        if "Kategori" in df.columns:
            revenue_category_pdf = (
                df.groupby("Kategori", as_index=False)[revenue_col]
                .sum()
                .sort_values(revenue_col, ascending=False)
            )

            fig_category_pdf = px.bar(
                revenue_category_pdf,
                x="Kategori",
                y=revenue_col,
                title="Revenue Berdasarkan Kategori"
            )

            add_chart_to_pdf("Revenue Berdasarkan Kategori", fig_category_pdf)

        if "Metode Pembayaran" in df.columns:
            payment_pdf = (
                df.groupby("Metode Pembayaran", as_index=False)[revenue_col]
                .sum()
                .sort_values(revenue_col, ascending=False)
            )

            fig_payment_pdf = px.pie(
                payment_pdf,
                names="Metode Pembayaran",
                values=revenue_col,
                title="Revenue Berdasarkan Metode Pembayaran"
            )

            add_chart_to_pdf("Revenue Berdasarkan Metode Pembayaran", fig_payment_pdf)

        if "Jam" in df.columns:
            revenue_hour_pdf = (
                df.groupby("Jam", as_index=False)[revenue_col]
                .sum()
                .sort_values("Jam")
            )

            fig_hour_pdf = px.bar(
                revenue_hour_pdf,
                x="Jam",
                y=revenue_col,
                title="Revenue Berdasarkan Jam"
            )

            add_chart_to_pdf("Revenue Berdasarkan Jam", fig_hour_pdf)

        logo_path = "assets/logo_toleransi.png"

        try:
            pdf_file = generate_pdf_report(
                total_revenue=total_revenue,
                total_transaksi=total_transaksi,
                total_qty=total_qty,
                avg_order=rata_transaksi,
                insights=insights,
                logo_path=logo_path if os.path.exists(logo_path) else None,
                chart_images=chart_images
            )

            st.download_button(
                label="📄 Download Executive Report PDF",
                data=pdf_file.getvalue(),
                file_name="toleransi_kopi_executive_report.pdf",
                mime="application/pdf"
            )

        except Exception as e:
            st.error(f"PDF gagal dibuat: {e}")