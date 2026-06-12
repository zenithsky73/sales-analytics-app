import os
import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
from utils.page_header import show_page_header
from utils.pdf_report import generate_premium_executive_report
from utils.ppt_report import generate_premium_ppt
from utils.helper import get_revenue_column, get_staff_column

def rupiah(value):
    return f"Rp {value:,.0f}".replace(",", ".")


def show_executive_report_page():

    show_page_header(
        "📊",
        "Executive Report Premium",
        "Laporan strategis untuk membantu owner mengambil keputusan bisnis."
    )

    if st.session_state.clean_data is None:
        st.warning("Upload dan cleaning data terlebih dahulu.")
        return

    df = st.session_state.clean_data.copy()

    # =========================
    # FILTER TANGGAL SAMA SEPERTI DASHBOARD
    # =========================
    if "Tanggal" in df.columns:
        df["Tanggal"] = pd.to_datetime(df["Tanggal"], errors="coerce")

        min_date = df["Tanggal"].min().date()
        max_date = df["Tanggal"].max().date()

        date_range = st.date_input(
            "Pilih Rentang Tanggal",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
            key="executive_date_filter"
        )

        if isinstance(date_range, tuple) and len(date_range) == 2:
            start_date, end_date = date_range

            df = df[
                (df["Tanggal"].dt.date >= start_date) &
                (df["Tanggal"].dt.date <= end_date)
            ]
    
    revenue_col = get_revenue_column(df)
    staff_col = get_staff_column(df)
    
    if "Kategori" in df.columns:
        kategori_list = sorted(df["Kategori"].dropna().unique())
        selected_kategori = st.multiselect(
            "Pilih Kategori",
            kategori_list,
            default=kategori_list,
            key="executive_kategori_filter"
        )
        df = df[df["Kategori"].isin(selected_kategori)]

    if "Metode Pembayaran" in df.columns:
        payment_list = sorted(df["Metode Pembayaran"].dropna().unique())
        selected_payment = st.multiselect(
            "Pilih Metode Pembayaran",
            payment_list,
            default=payment_list,
            key="executive_payment_filter"
        )
        df = df[df["Metode Pembayaran"].isin(selected_payment)]

    if staff_col:
        staff_list = sorted(df[staff_col].dropna().unique())
        selected_staff = st.multiselect(
            f"Pilih {staff_col}",
            staff_list,
            default=staff_list,
            key="executive_staff_filter"
        )
        df = df[df[staff_col].isin(selected_staff)]

    if revenue_col is None:
        st.error("Kolom revenue tidak ditemukan.")
        return

    total_revenue = df[revenue_col].sum()
    total_transaksi = df["Nomor"].nunique()
    total_item = df["Qty"].sum()
    aov = total_revenue / total_transaksi if total_transaksi > 0 else 0

    top_product = (
        df.groupby("Item")["Qty"]
        .sum()
        .sort_values(ascending=False)
        .head(1)
    )

    top_category = (
        df.groupby("Kategori")[revenue_col]
        .sum()
        .sort_values(ascending=False)
        .head(1)
    )

    top_hour = (
        df.groupby("Jam")[revenue_col]
        .sum()
        .sort_values(ascending=False)
        .head(1)
    )

    top_payment = (
        df.groupby("Metode Pembayaran")[revenue_col]
        .sum()
        .sort_values(ascending=False)
        .head(1)
    )

    st.subheader("📌 Executive Summary")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Revenue", rupiah(total_revenue))
    c2.metric("Total Transaksi", f"{total_transaksi:,}")
    c3.metric("Item Terjual", f"{total_item:,.0f}")
    c4.metric("Average Order", rupiah(aov))

    st.divider()

    st.subheader("🤖 AI Business Insight")

    st.info(f"""
    Pada periode data yang dianalisis, total revenue mencapai **{rupiah(total_revenue)}**
    dari **{total_transaksi:,} transaksi** dengan total **{total_item:,.0f} item terjual**.

    Produk terlaris adalah **{top_product.index[0]}** dengan total **{top_product.iloc[0]:,.0f} item**.

    Kategori dengan revenue tertinggi adalah **{top_category.index[0]}** sebesar **{rupiah(top_category.iloc[0])}**.

    Jam tersibuk terjadi pada pukul **{top_hour.index[0]}:00** dengan revenue **{rupiah(top_hour.iloc[0])}**.

    Metode pembayaran paling dominan adalah **{top_payment.index[0]}** dengan kontribusi revenue **{rupiah(top_payment.iloc[0])}**.
    """)

    st.subheader("☕ Product Performance")

    top_products = (
        df.groupby("Item")["Qty"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig_product = px.bar(
        top_products,
        x="Qty",
        y="Item",
        orientation="h",
        title="Top 10 Produk Terlaris"
    )

    st.plotly_chart(fig_product, width="stretch")

    st.subheader("📦 Category Performance")

    category_revenue = (
        df.groupby("Kategori")[revenue_col]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig_category = px.bar(
        category_revenue,
        x="Kategori",
        y=revenue_col,
        title="Top Revenue Berdasarkan Kategori"
    )

    st.plotly_chart(fig_category, width="stretch")

    st.subheader("⏰ Operational Analysis")

    hour_revenue = (
        df.groupby("Jam")[revenue_col]
        .sum()
        .reset_index()
    )

    fig_hour = px.bar(
        hour_revenue,
        x="Jam",
        y=revenue_col,
        title="Revenue Berdasarkan Jam"
    )

    st.plotly_chart(fig_hour, width="stretch")

    st.subheader("💳 Payment Analysis")

    payment_revenue = (
        df.groupby("Metode Pembayaran")[revenue_col]
        .sum()
        .reset_index()
    )

    fig_payment = px.pie(
        payment_revenue,
        names="Metode Pembayaran",
        values=revenue_col,
        title="Distribusi Revenue Berdasarkan Metode Pembayaran"
    )

    st.plotly_chart(fig_payment, width="stretch")

    st.subheader("🎯 Strategic Recommendation")

    recommendations = [
        f"Optimalkan stok produk **{top_product.index[0]}** karena menjadi produk dengan penjualan tertinggi.",
        f"Fokuskan promosi pada kategori **{top_category.index[0]}** karena memberikan revenue terbesar.",
        f"Tambahkan kesiapan operasional pada pukul **{top_hour.index[0]}:00** karena menjadi jam tersibuk.",
        f"Manfaatkan metode pembayaran **{top_payment.index[0]}** untuk program promo atau cashback.",
        "Gunakan hasil Apriori sebagai dasar membuat paket bundling produk.",
        "Evaluasi produk dengan penjualan rendah untuk strategi menu engineering."
    ]

    for rec in recommendations:
        st.success(f"✅ {rec}")

    st.divider()

    logo_path = "assets/logo_toleransi.png"

    pdf_file = generate_premium_executive_report(
        total_revenue=total_revenue,
        total_transaksi=total_transaksi,
        total_item=total_item,
        aov=aov,
        top_product=top_product.index[0],
        top_category=top_category.index[0],
        top_hour=top_hour.index[0],
        top_payment=top_payment.index[0],
        recommendations=recommendations,
        logo_path=logo_path if os.path.exists(logo_path) else None
    )

    chart_images = []

    def add_chart(title, fig):
        try:
            fig.update_layout(
                template="plotly_white",
                width=900,
                height=500,
                title=dict(text=title, x=0.5),
                margin=dict(l=60, r=40, t=80, b=80)
            )

            for trace in fig.data:
                if trace.type == "bar":
                    trace.marker.color = "#1E5FD8"
                elif trace.type == "scatter":
                    trace.line.color = "#1E5FD8"
                    trace.marker.color = "#1E5FD8"

            img_buffer = BytesIO()
            fig.write_image(img_buffer, format="png", scale=2)
            img_buffer.seek(0)

            chart_images.append((title, img_buffer))

        except Exception as e:
            st.warning(f"Grafik '{title}' gagal dimasukkan ke PDF: {e}")

    add_chart("Top 10 Produk Terlaris", fig_product)
    add_chart("Revenue Berdasarkan Kategori", fig_category)
    add_chart("Revenue Berdasarkan Jam", fig_hour)
    add_chart("Distribusi Metode Pembayaran", fig_payment)
    
    logo_path = "assets/logo_toleransi.png"

    st.download_button(
        label="📄 Download Executive Report Premium PDF",
        data=pdf_file.getvalue(),
        file_name="executive_report_premium_toleransi_kopi.pdf",
        mime="application/pdf",
        use_container_width=True
    )
    
    ppt_file = generate_premium_ppt(
        total_revenue=total_revenue,
        total_transaksi=total_transaksi,
        total_item=total_item,
        aov=aov,
        top_product=top_product.index[0],
        top_category=top_category.index[0],
        top_hour=top_hour.index[0],
        top_payment=top_payment.index[0],
        recommendations=recommendations,
        chart_images=chart_images,
        logo_path=logo_path if os.path.exists(logo_path) else None
    )

    st.download_button(
        label="📊 Download Executive Presentation PPTX",
        data=ppt_file.getvalue(),
        file_name="executive_presentation_toleransi_kopi.pptx",
        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        use_container_width=True
    )