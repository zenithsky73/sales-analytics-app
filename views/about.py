import streamlit as st


def show_about_page():

    st.markdown("""
    <style>
    .about-hero {
        background: linear-gradient(135deg, #1E5FD8, #3B82F6);
        padding: 35px;
        border-radius: 22px;
        color: white;
        box-shadow: 0px 10px 25px rgba(30,95,216,0.25);
        margin-bottom: 25px;
    }

    .about-card {
        background: white;
        border: 1px solid #E5E7EB;
        border-radius: 18px;
        padding: 24px;
        box-shadow: 0px 6px 18px rgba(15,23,42,0.08);
        height: 100%;
    }

    .about-title {
        font-size: 34px;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .about-subtitle {
        font-size: 16px;
        opacity: 0.9;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="about-hero">
        <div class="about-title">Toleransi Kopi Sales Analytics</div>
        <div class="about-subtitle">
            Aplikasi analisis data penjualan untuk membantu owner dan manager memahami performa bisnis secara lebih cepat dan akurat.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="about-card">
            <h3>🚀 Fitur Utama</h3>
            <ul>
                <li>Upload data CSV / Excel</li>
                <li>Data cleaning otomatis</li>
                <li>Dashboard KPI penjualan</li>
                <li>Visualisasi data interaktif</li>
                <li>Apriori Market Basket Analysis</li>
                <li>Forecast penjualan</li>
                <li>Export Executive Report PDF</li>
                <li>Profile Management</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="about-card">
            <h3>🛠️ Teknologi</h3>
            <ul>
                <li>Python</li>
                <li>Streamlit</li>
                <li>Pandas</li>
                <li>Plotly</li>
                <li>SQLite</li>
                <li>Mlxtend Apriori</li>
                <li>Scikit-learn</li>
                <li>ReportLab</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    col3, col4, col5 = st.columns(3)

    with col3:
        st.info("""
        **Versi**
        
        v1.0.0
        """)

    with col4:
        st.info("""
        **Developer**
        
        Muhammad Zeno Lidoviansa Putra
        """)

    with col5:
        st.info("""
        **Project Type**
        
        Sales Analytics
        """)

    st.info(
        "Project ini dibuat sebagai aplikasi analisis data penjualan berbasis Python dan Streamlit "
        "untuk mendukung pengambilan keputusan bisnis di Toleransi Kopi."
    )