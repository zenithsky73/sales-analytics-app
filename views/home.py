import streamlit as st
from utils.helper import get_revenue_column


def show_home_page():

    st.markdown(
        '<div class="header-container">'
        '<div class="header-title">📊 Sales Analytics Dashboard</div>'
        '<div class="header-subtitle">Toleransi Kopi Palagan</div>'
        '<div style="color:white;opacity:0.85;margin-top:6px;font-size:16px;">'
        'Analisis Data Transaksi Penjualan'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )
    
    st.markdown("""
    <style>
    .home-hero {
        background: linear-gradient(135deg, #1E5FD8, #3B82F6);
        color: white;
        padding: 42px;
        border-radius: 26px;
        box-shadow: 0px 15px 35px rgba(30,95,216,0.25);
        margin-bottom: 28px;
    }

    .home-title {
        font-size: 42px;
        font-weight: 900;
        margin-bottom: 8px;
    }

    .home-subtitle {
        font-size: 18px;
        opacity: 0.92;
        max-width: 750px;
        line-height: 1.6;
    }

    .feature-card {
        background: white;
        border: 1px solid #E5E7EB;
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0px 8px 22px rgba(15,23,42,0.08);
        height: 100%;
    }

    .feature-title {
        font-size: 22px;
        font-weight: 800;
        margin-bottom: 8px;
        color: #111827;
    }

    .feature-desc {
        color: #6B7280;
        line-height: 1.5;
    }
    </style>
    """, unsafe_allow_html=True)

    nama = st.session_state.get("nama", "User")

    st.markdown(f"""
    <div class="home-hero">
        <div class="home-title">Halo, {nama} 👋</div>
        <div class="home-subtitle">
            Selamat datang di <b>Toleransi Kopi Sales Analytics Platform</b>.
            Aplikasi ini membantu menganalisis data penjualan, menemukan pola pembelian,
            membuat forecast, dan menghasilkan laporan bisnis secara otomatis.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.clean_data is not None:
        df = st.session_state.clean_data.copy()
        revenue_col = get_revenue_column(df)

        total_revenue = df[revenue_col].sum() if revenue_col else 0
        total_transaksi = df["Nomor"].nunique() if "Nomor" in df.columns else 0
        total_qty = df["Qty"].sum() if "Qty" in df.columns else 0

        top_product = "-"
        if "Item" in df.columns and "Qty" in df.columns:
            top_product = (
                df.groupby("Item")["Qty"]
                .sum()
                .sort_values(ascending=False)
                .index[0]
            )

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Total Revenue", f"Rp {total_revenue:,.0f}")
        c2.metric("Total Transaksi", f"{total_transaksi:,}")
        c3.metric("Item Terjual", f"{total_qty:,.0f}")
        c4.metric("Top Product", top_product)

    else:
        st.info("Data belum tersedia. Silakan upload dan cleaning data terlebih dahulu untuk melihat ringkasan performa.")

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">📊 Dashboard KPI</div>
            <div class="feature-desc">
                Pantau revenue, transaksi, item terjual, average order value,
                kategori terbaik, dan jam penjualan tertinggi.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">🧠 Apriori Analysis</div>
            <div class="feature-desc">
                Temukan produk yang sering dibeli bersamaan untuk strategi
                bundling, cross-selling, dan promosi.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">📉 Forecast Sales</div>
            <div class="feature-desc">
                Prediksi potensi revenue beberapa hari ke depan menggunakan
                pendekatan data historis penjualan.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    col4, col5 = st.columns(2)

    with col4:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">📄 Executive Report</div>
            <div class="feature-desc">
                Export laporan PDF berisi KPI, insight bisnis, grafik,
                dan rekomendasi strategis untuk owner atau manager.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col5:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">👨‍💻 Developer</div>
            <div class="feature-desc">
                Muhammad Zeno Lidoviansa Putra<br>
                Data Analyst Enthusiast | Python Developer
            </div>
        </div>
        """, unsafe_allow_html=True)