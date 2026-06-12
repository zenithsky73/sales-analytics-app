import streamlit as st
from utils.helper import load_file
from utils.page_header import show_page_header



def show_upload_page():

    show_page_header(
        "📁",
        "Upload Data",
        "Upload file CSV atau Excel untuk memulai analisis."
    )

    uploaded_file = st.file_uploader(
        "Upload File CSV / Excel",
        type=["csv", "xlsx"]
    )

    if uploaded_file is not None:

        df = load_file(uploaded_file)

        st.session_state.raw_data = df

        # reset clean_data hanya saat file baru diupload
        st.session_state.clean_data = None

        st.success("File berhasil diupload.")
        st.toast("✅ Data berhasil diupload", icon="📁")

    if st.session_state.raw_data is not None:

        df = st.session_state.raw_data

        col1, col2 = st.columns(2)

        col1.metric("Jumlah Baris", df.shape[0])
        col2.metric("Jumlah Kolom", df.shape[1])

        st.subheader("Preview Data Mentah")

        st.dataframe(df, width="stretch")

    else:
        st.info("Silakan upload file CSV atau Excel terlebih dahulu.")