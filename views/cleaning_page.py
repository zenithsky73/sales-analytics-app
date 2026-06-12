import streamlit as st
import pandas as pd
from io import BytesIO
from utils.cleaning import clean_sales_data
from utils.page_header import show_page_header


def show_cleaning_page():

    show_page_header(
        "🧹",
        "Data Cleaning",
        "Membersihkan data agar siap digunakan dalam proses analisis."
    )

    if st.session_state.raw_data is None:
        st.warning("Upload data terlebih dahulu di menu Upload Data.")
        return

    df_clean = clean_sales_data(
        st.session_state.raw_data
    )

    st.session_state.clean_data = df_clean

    st.success("Data berhasil dibersihkan.")
    st.toast("✅ Data cleaning selesai", icon="🧹")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Baris Data Mentah",
        st.session_state.raw_data.shape[0]
    )

    col2.metric(
        "Baris Data Bersih",
        df_clean.shape[0]
    )

    col3.metric(
        "Jumlah Kolom",
        df_clean.shape[1]
    )

    st.subheader("Preview Data Bersih")

    st.dataframe(
        df_clean,
        width="stretch"
    )

    st.subheader("📋 Data Quality Report")

    missing_data = df_clean.isnull().sum()
    duplicate_data = df_clean.duplicated().sum()

    quality_col1, quality_col2, quality_col3 = st.columns(3)

    quality_col1.metric(
        "Missing Value",
        f"{missing_data.sum():,.0f}"
    )

    quality_col2.metric(
        "Duplicate Row",
        f"{duplicate_data:,.0f}"
    )

    quality_col3.metric(
        "Total Kolom",
        f"{df_clean.shape[1]:,.0f}"
    )

    missing_table = (
        missing_data
        .reset_index()
        .rename(columns={
            "index": "Kolom",
            0: "Jumlah Missing"
        })
    )

    st.dataframe(
        missing_table,
        width="stretch",
        hide_index=True
    )

    csv = df_clean.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Download Data Bersih CSV",
        data=csv,
        file_name="data_bersih_penjualan.csv",
        mime="text/csv"
    )

    excel_buffer = BytesIO()

    with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
        df_clean.to_excel(
            writer,
            index=False,
            sheet_name="Data Bersih"
        )

    st.download_button(
        label="Download Data Bersih Excel",
        data=excel_buffer.getvalue(),
        file_name="data_bersih_penjualan.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    
    