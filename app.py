import streamlit as st
import os
import base64

from views.executive_report import show_executive_report_page
from views.home import show_home_page
from views.about import show_about_page
from PIL import Image
from utils.auth import get_user_profile
from views.profile import show_profile_page
from views.login_page import show_login
from views.customer_segmentation import show_customer_segmentation_page
from views.forecast import show_forecast_page
from views.apriori_page import show_apriori_page
from utils.auth import init_db
from views.upload import show_upload_page
from views.cleaning_page import show_cleaning_page
from views.visualisasi import show_visualisasi_page
from views.dashboard import show_dashboard


# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Toleransi Kopi Analytics",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)

init_db()
LOGO_PATH = "assets/logo_toleransi.png"


# =========================
# DATABASE
# =========================
init_db()


# =========================
# SESSION STATE
# =========================
if "login" not in st.session_state:
    st.session_state.login = False

if "nama" not in st.session_state:
    st.session_state.nama = ""

if "jabatan" not in st.session_state:
    st.session_state.jabatan = ""

if "raw_data" not in st.session_state:
    st.session_state.raw_data = None

if "clean_data" not in st.session_state:
    st.session_state.clean_data = None


# =========================
# CSS
# =========================
st.markdown("""
<style>

/* =========================
   MAIN APP
========================= */
.stApp {
    background-color: #FFFFFF;
}

/* =========================
   SIDEBAR FIXED
========================= */
[data-testid="stSidebar"] {
    background-color: #F5F9FF;
    border-right: 2px solid #D6E4FF;
}

/* =========================
   HEADER
========================= */
.header-container {
    background: linear-gradient(135deg, #1E5FD8, #3B82F6);
    padding: 26px 30px;
    border-radius: 18px;
    margin-bottom: 25px;
    box-shadow: 0px 4px 14px rgba(30, 95, 216, 0.25);
}

.header-title {
    color: white;
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 4px;
}

.header-subtitle {
    color: white;
    opacity: 0.88;
    font-size: 18px;
}

/* =========================
   SIDEBAR BRAND
========================= */
.sidebar-logo-wrap {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 10px;
}

.sidebar-brand-title {
    text-align: center;
    color: #1E5FD8;
    font-size: 27px;
    font-weight: 800;
    margin-top: 8px;
}

.sidebar-brand-subtitle {
    text-align: center;
    color: #6B7280;
    font-size: 14px;
    margin-top: 3px;
}

/* =========================
   USER CARD
========================= */
.user-card {
    background: white;
    padding: 15px 17px;
    border-radius: 16px;
    border-left: 5px solid #1E5FD8;
    box-shadow: 0px 2px 8px rgba(30, 95, 216, 0.10);
    line-height: 1.8;
}

/* =========================
   MENU
========================= */
.menu-title {
    font-size: 13px;
    font-weight: 800;
    color: #64748B;
    letter-spacing: 0.5px;
    margin-bottom: 12px;
}

[data-testid="stSidebar"] div[role="radiogroup"] {
    width: 100% !important;
}

[data-testid="stSidebar"] div[role="radiogroup"] > div {
    width: 100% !important;
}

[data-testid="stSidebar"] div[role="radiogroup"] label {
    width: 100% !important;
    min-width: 100% !important;

    background: white;
    border-radius: 16px;
    padding: 16px 20px;
    margin-bottom: 14px;

    border: 1px solid #E5E7EB;
    box-shadow: 0px 3px 10px rgba(0,0,0,0.06);

    display: flex !important;
    align-items: center !important;
    justify-content: flex-start !important;

    transition: all 0.2s ease;
}

[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
    background: #EEF5FF;
    border-color: #1E5FD8;
}

[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {
    background: #1E5FD8 !important;
    border-color: #1E5FD8 !important;
    box-shadow: 0px 6px 16px rgba(30,95,216,.30);
}

[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) * {
    color: white !important;
    font-weight: 800 !important;
}

[data-testid="stSidebar"] div[role="radiogroup"] label > div:first-child {
    display: none;
}

[data-testid="stSidebar"] div[role="radiogroup"] label div {
    width: 100% !important;
}

/* =========================
   KPI CARD
========================= */
[data-testid="metric-container"] {
    background: white;
    border: 1px solid #D6E4FF;
    padding: 16px;
    border-radius: 15px;
    box-shadow: 0px 2px 8px rgba(30, 95, 216, 0.08);
}

/* =========================
   BUTTON
========================= */
.stButton > button {
    border-radius: 12px;
    font-weight: 700;
}

[data-testid="stSidebar"] div[role="radiogroup"] label {

    width: 100% !important;

    background: white;
    border-radius: 18px;

    padding: 16px 18px;

    margin-bottom: 14px;

    border-left: 4px solid transparent;

    box-shadow: 0px 3px 10px rgba(0,0,0,0.06);

    transition: all 0.2s ease;
}

[data-testid="stSidebar"] div[role="radiogroup"] label:hover {

    border-left: 4px solid #2563EB;

    transform: translateX(3px);
}

[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {

    background: #2563EB !important;

    border-left: 4px solid #1D4ED8;

    box-shadow: 0px 8px 20px rgba(37,99,235,0.30);
}

[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) * {

    color: white !important;
    font-weight: 700 !important;
}

[data-testid="stSidebar"] .stButton > button:hover {
    background: #1E5FD8;
    color: white;
    border-color: #1E5FD8;
}

/* =========================
   FILE UPLOADER
========================= */
[data-testid="stFileUploader"] {
    border: 2px dashed #1E5FD8;
    border-radius: 12px;
    padding: 10px;
}

h1, h2, h3 {
    color: #1E5FD8;
}

.profile-menu-card {
    display: flex;
    align-items: center;
    gap: 12px;
    background: white;
    border: 1px solid #D6E4FF;
    border-radius: 18px;
    padding: 10px 14px;
    box-shadow: 0px 4px 14px rgba(30,95,216,0.12);
}

.profile-avatar {
    width: 46px;
    height: 46px;
    border-radius: 50%;
    object-fit: cover;
    border: 3px solid #1E5FD8;
}

.profile-avatar-default {
    width: 46px;
    height: 46px;
    border-radius: 50%;
    background: #EAF2FF;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 3px solid #1E5FD8;
}

/* =========================
   RESPONSIVE MOBILE
========================= */
@media (max-width: 768px) {

    .block-container {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        padding-top: 1rem !important;
    }

    [data-testid="stHorizontalBlock"] {
        flex-direction: column !important;
    }

    [data-testid="column"] {
        width: 100% !important;
        flex: 1 1 100% !important;
        margin-bottom: 1rem !important;
    }

    .header-title {
        font-size: 28px !important;
    }

    .header-subtitle {
        font-size: 14px !important;
    }

    .profile-menu-card {
        width: 100% !important;
    }

    [data-testid="metric-container"] {
        width: 100% !important;
    }

    iframe {
        width: 100% !important;
    }
}
</style>
""", unsafe_allow_html=True)


# =========================
# LOGIN PAGE
# =========================
if not st.session_state.login:
    show_login()
    st.stop()

# =========================
# SIDEBAR BRAND
# =========================
if os.path.exists(LOGO_PATH):
    col1, col2, col3 = st.sidebar.columns([1, 2, 1])

with col2:
    st.image(LOGO_PATH, width=170)

st.sidebar.markdown(
    """
    <div class="sidebar-brand-title">Toleransi Kopi</div>
    <div class="sidebar-brand-subtitle">Sales Analytics Platform</div>
    """,
    unsafe_allow_html=True
)

st.sidebar.divider()

st.sidebar.markdown(
    f"""
    <div class="user-card">
        <b>👤 {st.session_state.nama}</b><br>
        <span style="color:#6B7280;">🏷️ {st.session_state.jabatan}</span>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.divider()

# =========================
# SIDEBAR MENU BUTTON
# =========================
if "menu" not in st.session_state:
    st.session_state.menu = "🏠 Home"

st.sidebar.markdown(
    """
    <div class="menu-title">MENU UTAMA</div>
    """,
    unsafe_allow_html=True
)

def menu_button(label):
    active = st.session_state.menu == label

    button_class = "menu-button active" if active else "menu-button"

    if st.sidebar.button(label, key=label, use_container_width=True):
        st.session_state.menu = label
        st.session_state.account_page = None
        st.rerun()

jabatan = st.session_state.jabatan.lower()

if jabatan in ["owner", "manager", "admin"]:

    menu_button("🏠 Home")
    menu_button("📊 Dashboard")
    menu_button("📁 Upload Data")
    menu_button("🧹 Data Cleaning")
    menu_button("📊 Visualisasi Data")
    menu_button("🧠 Apriori")
    menu_button("📉 Forecast")
    menu_button("👥 Customer")
    menu_button("ℹ️ About")
    menu_button("📊 Executive Report")
    
else:

    menu_button("🏠 Home")
    menu_button("📊 Dashboard")    
    menu_button("📁 Upload Data")
    menu_button("🧹 Data Cleaning")
    menu_button("📊 Visualisasi Data")
    menu_button("ℹ️ About")

menu = st.session_state.menu

st.sidebar.markdown("<br>", unsafe_allow_html=True)

# =========================
# TOP RIGHT ACCOUNT MENU
# =========================
if "account_page" not in st.session_state:
    st.session_state.account_page = None

if "username" not in st.session_state:
    st.session_state.username = ""

def image_to_base64(path):
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()


top_left, top_right = st.columns([7, 3])

with top_right:
    user_profile = get_user_profile(st.session_state.username)
    foto_profil = user_profile[5] if user_profile else None

    if foto_profil and os.path.exists(foto_profil):
        img_base64 = image_to_base64(foto_profil)
        img_html = f"<img class='profile-avatar' src='data:image/png;base64,{img_base64}'>"
    else:
        img_html = "<div class='profile-avatar-default'>👤</div>"

    with st.popover(f"👤 {st.session_state.nama}"):
        st.markdown(
            f"""
            <div class="profile-menu-card">
                {img_html}
                <div>
                    <b>{st.session_state.nama}</b><br>
                    <span>{st.session_state.jabatan}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button("👤 My Profile", use_container_width=True):
            st.session_state.account_page = "profile"
            st.rerun()

        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.clear()
            st.rerun()

# =========================
# ROUTER
# =========================
if st.session_state.account_page == "profile":
    show_profile_page()
    st.stop()

if menu == "🏠 Home":
    show_home_page()
    
elif menu == "📊 Dashboard":
    show_dashboard()

elif menu == "📁 Upload Data":
    show_upload_page()

elif menu == "🧹 Data Cleaning":
    show_cleaning_page()

elif menu == "📊 Visualisasi Data":
    show_visualisasi_page()

elif menu == "🧠 Apriori":
    show_apriori_page()

elif menu == "📉 Forecast":
    show_forecast_page()
    
elif menu == "👥 Customer":
    show_customer_segmentation_page()
    
elif menu == "ℹ️ About":
    show_about_page()
    
elif menu == "📊 Executive Report":
    show_executive_report_page()