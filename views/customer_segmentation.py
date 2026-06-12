import streamlit as st
import pandas as pd
import plotly.express as px

from utils.helper import get_revenue_column
from utils.page_header import show_page_header


def show_customer_segmentation_page():

    show_page_header(
        "👥",
        "Customer Segmentation",
        "Mengelompokkan pelanggan berdasarkan perilaku transaksi."
    )

    if st.session_state.clean_data is None:
        st.warning("Lakukan data cleaning terlebih dahulu.")
        return

    df = st.session_state.clean_data.copy()
    revenue_col = get_revenue_column(df)

    if revenue_col is None:
        st.error("Kolom revenue tidak ditemukan.")
        return

    if "Pelanggan" not in df.columns or "Nomor" not in df.columns:
        st.error("Kolom Pelanggan dan Nomor wajib tersedia.")
        return

    customer_df = (
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
    )

    def segment_customer(row):
        if row["Total Revenue"] >= customer_df["Total Revenue"].quantile(0.75):
            return "VIP Customer"
        elif row["Total Transaksi"] >= customer_df["Total Transaksi"].quantile(0.50):
            return "Regular Customer"
        else:
            return "New / Low Customer"

    customer_df["Segment"] = customer_df.apply(segment_customer, axis=1)

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Customer", customer_df["Pelanggan"].nunique())
    col2.metric("VIP Customer", (customer_df["Segment"] == "VIP Customer").sum())
    col3.metric("Regular Customer", (customer_df["Segment"] == "Regular Customer").sum())

    st.subheader("Distribusi Segment Customer")

    segment_count = (
        customer_df.groupby("Segment", as_index=False)["Pelanggan"]
        .count()
        .rename(columns={"Pelanggan": "Jumlah Customer"})
    )

    fig_segment = px.pie(
        segment_count,
        names="Segment",
        values="Jumlah Customer",
        title="Distribusi Customer Segment"
    )

    st.plotly_chart(fig_segment, width="stretch")

    st.subheader("Customer Segmentation Table")

    st.dataframe(
        customer_df.sort_values("Total Revenue", ascending=False),
        width="stretch",
        hide_index=True
    )

    st.subheader("Insight Customer")

    top_customer = customer_df.sort_values("Total Revenue", ascending=False).iloc[0]

    st.success(
        f"Customer dengan revenue tertinggi adalah **{top_customer['Pelanggan']}** "
        f"dengan total revenue **Rp {top_customer['Total Revenue']:,.0f}** "
        f"dan masuk segment **{top_customer['Segment']}**."
    )