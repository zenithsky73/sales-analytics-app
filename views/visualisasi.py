import streamlit as st
import plotly.express as px

from utils.page_header import show_page_header
from utils.helper import get_revenue_column, get_staff_column


def show_visualisasi_page():

    show_page_header(
        "📈",
        "Visualisasi Data",
        "Eksplorasi grafik dan tren penjualan."
    )

    if st.session_state.clean_data is None:
        st.warning("Lakukan data cleaning terlebih dahulu.")
        return

    df = st.session_state.clean_data.copy()

    revenue_col = get_revenue_column(df)
    staff_col = get_staff_column(df)

    if revenue_col is None:
        st.error("Kolom revenue tidak ditemukan.")
        return

    st.info(
        "Halaman ini menampilkan visualisasi lengkap dari data penjualan yang sudah dibersihkan."
    )

    # =========================
    # FILTER VISUALISASI
    # =========================
    st.sidebar.subheader("Filter Visualisasi")

    if "Tanggal_Hari" in df.columns:
        df = df.dropna(subset=["Tanggal_Hari"])

        if not df.empty:
            tanggal_min = df["Tanggal_Hari"].min()
            tanggal_max = df["Tanggal_Hari"].max()

            tanggal_filter = st.sidebar.date_input(
                "Pilih Rentang Tanggal",
                value=(tanggal_min, tanggal_max),
                min_value=tanggal_min,
                max_value=tanggal_max,
                key="visual_tanggal"
            )

            if len(tanggal_filter) == 2:
                start_date, end_date = tanggal_filter
                df = df[
                    (df["Tanggal_Hari"] >= start_date) &
                    (df["Tanggal_Hari"] <= end_date)
                ]

    if "Kategori" in df.columns:
        kategori_list = sorted(df["Kategori"].dropna().unique())
        selected_kategori = st.sidebar.multiselect(
            "Pilih Kategori",
            kategori_list,
            default=kategori_list,
            key="visual_kategori"
        )
        df = df[df["Kategori"].isin(selected_kategori)]

    if staff_col:
        staff_list = sorted(df[staff_col].dropna().unique())
        selected_staff = st.sidebar.multiselect(
            f"Pilih {staff_col}",
            staff_list,
            default=staff_list,
            key="visual_staff"
        )
        df = df[df[staff_col].isin(selected_staff)]

    if "Metode Pembayaran" in df.columns:
        payment_list = sorted(df["Metode Pembayaran"].dropna().unique())
        selected_payment = st.sidebar.multiselect(
            "Pilih Metode Pembayaran",
            payment_list,
            default=payment_list,
            key="visual_payment"
        )
        df = df[df["Metode Pembayaran"].isin(selected_payment)]

    if df.empty:
        st.warning("Tidak ada data berdasarkan filter yang dipilih.")
        return

    # =========================
    # ROW 1
    # =========================
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("1. Revenue Harian")

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

    with col2:
        st.subheader("2. Total Transaksi Harian")

        if "Tanggal_Hari" in df.columns and "Nomor" in df.columns:
            trx_daily = (
                df.groupby("Tanggal_Hari", as_index=False)["Nomor"]
                .nunique()
                .rename(columns={"Nomor": "Total Transaksi"})
            )

            fig_trx_daily = px.line(
                trx_daily,
                x="Tanggal_Hari",
                y="Total Transaksi",
                markers=True,
                title="Total Transaksi per Hari"
            )

            st.plotly_chart(
                fig_trx_daily,
                width="stretch"
            )

    # =========================
    # ROW 2
    # =========================
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("3. Top 10 Produk Terlaris")

        if "Item" in df.columns and "Qty" in df.columns:
            top_items_qty = (
                df.groupby("Item", as_index=False)["Qty"]
                .sum()
                .sort_values("Qty", ascending=False)
                .head(10)
            )

            fig_items_qty = px.bar(
                top_items_qty,
                x="Qty",
                y="Item",
                orientation="h",
                title="Top 10 Produk Berdasarkan Qty"
            )

            st.plotly_chart(
                fig_items_qty,
                width="stretch"
            )

    with col4:
        st.subheader("4. Top 10 Produk by Revenue")

        if "Item" in df.columns:
            top_items_revenue = (
                df.groupby("Item", as_index=False)[revenue_col]
                .sum()
                .sort_values(revenue_col, ascending=False)
                .head(10)
            )

            fig_items_revenue = px.bar(
                top_items_revenue,
                x=revenue_col,
                y="Item",
                orientation="h",
                title="Top 10 Produk Berdasarkan Revenue"
            )

            st.plotly_chart(
                fig_items_revenue,
                width="stretch"
            )

    # =========================
    # ROW 3
    # =========================
    col5, col6 = st.columns(2)

    with col5:
        st.subheader("5. Revenue by Category")

        if "Kategori" in df.columns:
            category_sales = (
                df.groupby("Kategori", as_index=False)[revenue_col]
                .sum()
                .sort_values(revenue_col, ascending=False)
            )

            fig_category = px.bar(
                category_sales,
                x="Kategori",
                y=revenue_col,
                title="Revenue Berdasarkan Kategori"
            )

            st.plotly_chart(
                fig_category,
                width="stretch"
            )

    with col6:
        st.subheader("6. Category Share")

        if "Kategori" in df.columns:
            category_share = (
                df.groupby("Kategori", as_index=False)[revenue_col]
                .sum()
                .sort_values(revenue_col, ascending=False)
            )

            fig_category_pie = px.pie(
                category_share,
                names="Kategori",
                values=revenue_col,
                title="Persentase Revenue per Kategori"
            )

            st.plotly_chart(
                fig_category_pie,
                width="stretch"
            )

    # =========================
    # ROW 4
    # =========================
    col7, col8 = st.columns(2)

    with col7:
        st.subheader("7. Revenue by Payment Method")

        if "Metode Pembayaran" in df.columns:
            payment_sales = (
                df.groupby("Metode Pembayaran", as_index=False)[revenue_col]
                .sum()
                .sort_values(revenue_col, ascending=False)
            )

            fig_payment = px.bar(
                payment_sales,
                x="Metode Pembayaran",
                y=revenue_col,
                title="Revenue Berdasarkan Metode Pembayaran"
            )

            st.plotly_chart(
                fig_payment,
                width="stretch"
            )

    with col8:
        st.subheader("8. Payment Method Share")

        if "Metode Pembayaran" in df.columns:
            payment_share = (
                df.groupby("Metode Pembayaran", as_index=False)[revenue_col]
                .sum()
                .sort_values(revenue_col, ascending=False)
            )

            fig_payment_pie = px.pie(
                payment_share,
                names="Metode Pembayaran",
                values=revenue_col,
                title="Persentase Revenue per Metode Pembayaran"
            )

            st.plotly_chart(
                fig_payment_pie,
                width="stretch"
            )

    # =========================
    # ROW 5
    # =========================
    col9, col10 = st.columns(2)

    with col9:
        st.subheader("9. Revenue by Hour")

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
                title="Revenue Berdasarkan Jam"
            )

            st.plotly_chart(
                fig_hour,
                width="stretch"
            )

    with col10:
        st.subheader("10. Qty Sold by Hour")

        if "Jam" in df.columns and "Qty" in df.columns:
            qty_hour = (
                df.groupby("Jam", as_index=False)["Qty"]
                .sum()
                .sort_values("Jam")
            )

            fig_qty_hour = px.bar(
                qty_hour,
                x="Jam",
                y="Qty",
                title="Jumlah Item Terjual Berdasarkan Jam"
            )

            st.plotly_chart(
                fig_qty_hour,
                width="stretch"
            )

    # =========================
    # ROW 6
    # =========================
    col11, col12 = st.columns(2)

    with col11:
        st.subheader(f"11. Revenue by {staff_col}")

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

    with col12:
        st.subheader(f"12. Transaction by {staff_col}")

        if staff_col and "Nomor" in df.columns:
            staff_trx = (
                df.groupby(staff_col, as_index=False)["Nomor"]
                .nunique()
                .rename(columns={"Nomor": "Total Transaksi"})
                .sort_values("Total Transaksi", ascending=False)
            )

            fig_staff_trx = px.bar(
                staff_trx,
                x=staff_col,
                y="Total Transaksi",
                title=f"Total Transaksi Berdasarkan {staff_col}"
            )

            st.plotly_chart(
                fig_staff_trx,
                width="stretch"
            )

    # =========================
    # ROW 7
    # =========================
    col13, col14 = st.columns(2)

    with col13:
        st.subheader("13. Top 10 Pelanggan by Revenue")

        if "Pelanggan" in df.columns:
            customer_sales = (
                df.groupby("Pelanggan", as_index=False)[revenue_col]
                .sum()
                .sort_values(revenue_col, ascending=False)
                .head(10)
            )

            fig_customer = px.bar(
                customer_sales,
                x=revenue_col,
                y="Pelanggan",
                orientation="h",
                title="Top 10 Pelanggan Berdasarkan Revenue"
            )

            st.plotly_chart(
                fig_customer,
                width="stretch"
            )

    with col14:
        st.subheader("14. Top 10 Pelanggan by Transaction")

        if "Pelanggan" in df.columns and "Nomor" in df.columns:
            customer_trx = (
                df.groupby("Pelanggan", as_index=False)["Nomor"]
                .nunique()
                .rename(columns={"Nomor": "Total Transaksi"})
                .sort_values("Total Transaksi", ascending=False)
                .head(10)
            )

            fig_customer_trx = px.bar(
                customer_trx,
                x="Total Transaksi",
                y="Pelanggan",
                orientation="h",
                title="Top 10 Pelanggan Berdasarkan Transaksi"
            )

            st.plotly_chart(
                fig_customer_trx,
                width="stretch"
            )

    # =========================
    # ROW 8
    # =========================
    col15, col16 = st.columns(2)

    with col15:
        st.subheader("15. Revenue by Sales Type")

        if "Tipe Penjualan" in df.columns:
            sales_type = (
                df.groupby("Tipe Penjualan", as_index=False)[revenue_col]
                .sum()
                .sort_values(revenue_col, ascending=False)
            )

            fig_sales_type = px.bar(
                sales_type,
                x="Tipe Penjualan",
                y=revenue_col,
                title="Revenue Berdasarkan Tipe Penjualan"
            )

            st.plotly_chart(
                fig_sales_type,
                width="stretch"
            )

    with col16:
        st.subheader("16. Revenue by Variant")

        if "Varian" in df.columns:
            variant_sales = (
                df.groupby("Varian", as_index=False)[revenue_col]
                .sum()
                .sort_values(revenue_col, ascending=False)
                .head(10)
            )

            fig_variant = px.bar(
                variant_sales,
                x=revenue_col,
                y="Varian",
                orientation="h",
                title="Top Varian Berdasarkan Revenue"
            )

            st.plotly_chart(
                fig_variant,
                width="stretch"
            )
            
        # =========================
    # ROW 9 - HEATMAP
    # =========================
    st.subheader("17. Heatmap Revenue Hari × Jam")

    if "Tanggal" in df.columns and "Jam" in df.columns:
        df["Nama_Hari"] = df["Tanggal"].dt.day_name()

        hari_mapping = {
            "Monday": "Senin",
            "Tuesday": "Selasa",
            "Wednesday": "Rabu",
            "Thursday": "Kamis",
            "Friday": "Jumat",
            "Saturday": "Sabtu",
            "Sunday": "Minggu"
        }

        df["Nama_Hari"] = df["Nama_Hari"].map(hari_mapping)

        heatmap_data = (
            df.groupby(["Nama_Hari", "Jam"], as_index=False)[revenue_col]
            .sum()
        )

        hari_order = [
            "Senin",
            "Selasa",
            "Rabu",
            "Kamis",
            "Jumat",
            "Sabtu",
            "Minggu"
        ]

        heatmap_pivot = heatmap_data.pivot(
            index="Nama_Hari",
            columns="Jam",
            values=revenue_col
        ).reindex(hari_order)

        fig_heatmap = px.imshow(
            heatmap_pivot,
            labels=dict(
                x="Jam",
                y="Hari",
                color="Revenue"
            ),
            title="Heatmap Revenue Berdasarkan Hari dan Jam"
        )

        st.plotly_chart(
            fig_heatmap,
            width="stretch"
        )        
        
        # =========================
    # CUSTOMER ANALYSIS
    # =========================
    st.subheader("18. Customer Analysis")

    if "Pelanggan" in df.columns and "Nomor" in df.columns:

        customer_summary = (
            df.groupby("Pelanggan", as_index=False)
            .agg({
                "Nomor": "nunique",
                revenue_col: "sum",
                "Qty": "sum"
            })
            .rename(columns={
                "Nomor": "Total Transaksi",
                revenue_col: "Total Revenue",
                "Qty": "Total Qty"
            })
            .sort_values("Total Revenue", ascending=False)
        )

        st.dataframe(
            customer_summary.head(20),
            width="stretch",
            hide_index=True
        )
