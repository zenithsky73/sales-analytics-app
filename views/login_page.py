import streamlit as st
from utils.auth import login_user, register_user, verify_user_email, reset_user_password


def valid_password(password):
    return (
        len(password) >= 8
        and any(char.isupper() for char in password)
        and any(char.isdigit() for char in password)
    )


def show_login():
    if "auth_mode" not in st.session_state:
        st.session_state.auth_mode = "login"

    st.markdown("""
    <style>
    [data-testid="stSidebar"] { display: none; }

    .stApp {
        background: linear-gradient(135deg, #EEF5FF, #FFFFFF);
    }

    .block-container {
        padding-top: 5rem;
        max-width: 1150px;
    }

    div[data-testid="stHorizontalBlock"] {
        background: white;
        border-radius: 32px;
        box-shadow: 0px 20px 50px rgba(15, 23, 42, 0.18);
        padding: 0px 0px 0px 60px;
        overflow: hidden;
        min-height: 560px;
    }

    div[data-testid="column"] {
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    .brand-login {
        color: #1E5FD8;
        font-size: 23px;
        font-weight: 800;
        margin-bottom: 35px;
    }

    .auth-title {
        font-size: 42px;
        font-weight: 800;
        color: #111827;
        margin-bottom: 10px;
    }

    .auth-desc {
        color: #6B7280;
        font-size: 16px;
        margin-bottom: 28px;
    }

    .auth-panel {
        background: linear-gradient(135deg, #1E5FD8, #3B82F6);
        color: white;
        min-height: 560px;
        border-radius: 150px 32px 32px 150px;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
    }

    .right-title {
        font-size: 38px;
        font-weight: 800;
        margin-bottom: 18px;
    }

    .right-desc {
        font-size: 17px;
        opacity: 0.92;
        line-height: 1.6;
        padding: 0 35px;
    }

    .stTextInput input {
        border-radius: 12px;
        height: 48px;
        background-color: #F1F5F9;
    }

    .stButton > button {
        background: #1E5FD8;
        color: white;
        border-radius: 12px;
        border: none;
        height: 48px;
        font-weight: 800;
    }

    .stButton > button:hover {
        background: #1548A8;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

    left, right = st.columns([1.05, 1], gap="large")

    with left:
        st.markdown(
            "<div class='brand-login'>☕ Toleransi Kopi Analytics</div>",
            unsafe_allow_html=True
        )

        if st.session_state.auth_mode == "login":
            st.markdown("<div class='auth-title'>Sign In</div>", unsafe_allow_html=True)
            st.markdown("<div class='auth-desc'>Masuk ke aplikasi analisis data penjualan.</div>", unsafe_allow_html=True)

            username = st.text_input("Username", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")

            if st.button("SIGN IN", use_container_width=True, key="login_button"):
                user = login_user(username, password)

                if user:
                    st.session_state.login = True
                    st.session_state.nama = user[0]
                    st.session_state.jabatan = user[1]
                    st.session_state.username = username
                    st.rerun()
                else:
                    st.error("Username atau password salah.")

            if st.button("Lupa Password?", key="forgot_password_button", type="secondary"):
                st.session_state.auth_mode = "forgot_password"
                st.rerun()

        elif st.session_state.auth_mode == "register":
            st.markdown("<div class='auth-title'>Create Account</div>", unsafe_allow_html=True)
            st.markdown("<div class='auth-desc'>Daftarkan akun baru untuk mengakses dashboard.</div>", unsafe_allow_html=True)

            nama = st.text_input("Nama Lengkap", key="register_nama")
            jenis_kelamin = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"], key="register_gender")
            jabatan = st.selectbox("Jabatan", ["Owner", "Manager", "Admin", "Kasir", "Barista", "Staff"], key="register_jabatan")
            email = st.text_input("Email", key="register_email")
            username = st.text_input("Username", key="register_username")
            password = st.text_input("Password", type="password", key="register_password")

            st.markdown("""
            <div style="
                background:#EFF6FF;
                padding:12px;
                border-radius:10px;
                border-left:4px solid #1E5FD8;
                margin-bottom:15px;
                font-size:14px;
                color:#1E293B;
            ">
            🔒 <b>Syarat Password</b><br>
            • Minimal 8 karakter<br>
            • Mengandung minimal 1 huruf besar (A-Z)<br>
            • Mengandung minimal 1 angka (0-9)
            </div>
            """, unsafe_allow_html=True)

            confirm_password = st.text_input("Konfirmasi Password", type="password", key="register_confirm_password")

            if st.button("SIGN UP", use_container_width=True, key="register_button"):
                if not nama or not jabatan or not email or not username or not password or not confirm_password:
                    st.warning("Semua field wajib diisi.")
                elif not valid_password(password):
                    st.error("Password minimal 8 karakter, memiliki 1 huruf besar, dan 1 angka.")
                elif password != confirm_password:
                    st.error("Konfirmasi password tidak sama.")
                else:
                    success = register_user(nama, jenis_kelamin, jabatan, email, username, password)

                    if success:
                        st.success("Akun berhasil dibuat. Silakan login.")
                        st.session_state.auth_mode = "login"
                        st.rerun()
                    else:
                        st.error("Username sudah digunakan.")

        elif st.session_state.auth_mode == "forgot_password":
            st.markdown("<div class='auth-title'>Forgot Password</div>", unsafe_allow_html=True)
            st.markdown("<div class='auth-desc'>Masukkan username dan email yang terdaftar.</div>", unsafe_allow_html=True)

            username = st.text_input("Username", key="forgot_username")
            email = st.text_input("Email Terdaftar", key="forgot_email")

            if st.button("VERIFIKASI AKUN", use_container_width=True, key="verify_button"):
                if verify_user_email(username, email):
                    st.session_state.reset_username = username
                    st.session_state.auth_mode = "reset_password"
                    st.rerun()
                else:
                    st.error("Username atau email tidak cocok.")

            if st.button("← Kembali ke Login", key="back_login_1"):
                st.session_state.auth_mode = "login"
                st.rerun()

        elif st.session_state.auth_mode == "reset_password":
            st.markdown("<div class='auth-title'>Reset Password</div>", unsafe_allow_html=True)
            st.markdown("<div class='auth-desc'>Buat password baru untuk akun Anda.</div>", unsafe_allow_html=True)

            new_password = st.text_input("Password Baru", type="password", key="reset_password")
            confirm_password = st.text_input("Konfirmasi Password Baru", type="password", key="reset_confirm_password")

            st.markdown("""
            <div style="
                background:#EFF6FF;
                padding:12px;
                border-radius:10px;
                border-left:4px solid #1E5FD8;
                margin-bottom:15px;
                font-size:14px;
                color:#1E293B;
            ">
            🔒 Password minimal 8 karakter, mengandung 1 huruf besar, dan 1 angka.
            </div>
            """, unsafe_allow_html=True)

            if st.button("SIMPAN PASSWORD BARU", use_container_width=True, key="reset_button"):
                if not new_password or not confirm_password:
                    st.warning("Semua field wajib diisi.")
                elif not valid_password(new_password):
                    st.error("Password belum memenuhi syarat.")
                elif new_password != confirm_password:
                    st.error("Konfirmasi password tidak sama.")
                else:
                    reset_user_password(
                        st.session_state.reset_username,
                        new_password
                    )

                    st.success("Password berhasil direset. Silakan login.")
                    st.session_state.auth_mode = "login"
                    st.rerun()

            if st.button("← Kembali ke Login", key="back_login_2"):
                st.session_state.auth_mode = "login"
                st.rerun()

    with right:
        if st.session_state.auth_mode == "login":
            title = "Hello, Friend!"
            desc = "Belum punya akun? Daftar terlebih dahulu untuk menggunakan semua fitur."
            button_label = "SIGN UP"
            target_mode = "register"

        elif st.session_state.auth_mode == "register":
            title = "Start Your Analytics!"
            desc = "Daftarkan akun dan mulai pantau performa penjualan dengan lebih mudah."
            button_label = "Sudah punya akun? Masuk"
            target_mode = "login"

        elif st.session_state.auth_mode in ["forgot_password", "reset_password"]:
            title = "Account Recovery"
            desc = "Verifikasi akun Anda dan buat password baru dengan aman."
            button_label = "BACK TO LOGIN"
            target_mode = "login"

        st.markdown(f"""
        <div class="auth-panel">
            <div>
                <div class="right-title">{title}</div>
                <div class="right-desc">{desc}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button(button_label, use_container_width=True, key="switch_auth_mode"):
            st.session_state.auth_mode = target_mode
            st.rerun()