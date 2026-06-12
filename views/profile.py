import streamlit as st
import os
import base64
from PIL import Image
from utils.page_header import show_page_header
from utils.auth import (
    get_user_profile,
    update_user_profile,
    change_password
)

def image_to_base64(path):
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()


def save_profile_photo(uploaded_file, username):
    os.makedirs("assets/profile", exist_ok=True)

    image = Image.open(uploaded_file).convert("RGB")

    width, height = image.size
    min_side = min(width, height)

    left = (width - min_side) // 2
    top = (height - min_side) // 2
    right = left + min_side
    bottom = top + min_side

    image = image.crop((left, top, right, bottom))
    image = image.resize((400, 400))

    foto_path = f"assets/profile/{username}.png"
    image.save(foto_path)

    return foto_path


def show_profile_page():

    show_page_header(
        "👤",
        "My Profile",
        "Kelola informasi akun, foto profil, dan keamanan akun."
    )

    if "username" not in st.session_state or not st.session_state.username:
        st.warning("Data user tidak ditemukan. Silakan login ulang.")
        return

    username = st.session_state.username
    user = get_user_profile(username)

    if not user:
        st.error("Profile tidak ditemukan.")
        return

    nama, jenis_kelamin, jabatan, email, username, foto_profil = user

    tab_info, tab_security = st.tabs([
        "👤 Informasi Akun",
        "🔑 Keamanan"
    ])

    with tab_info:

        col_left, col_right = st.columns([1, 2], gap="large")

        uploaded_file = None

        with col_left:
            st.subheader("Foto Profil")

            if foto_profil and os.path.exists(foto_profil):
                st.image(foto_profil, width=180)
            else:
                st.image(
                    "https://cdn-icons-png.flaticon.com/512/149/149071.png",
                    width=180
                )

            uploaded_file = st.file_uploader(
                "📷 Ubah Foto Profil",
                type=["jpg", "jpeg", "png"]
            )

            st.info("Foto akan otomatis disesuaikan menjadi bentuk bulat.")

            st.markdown(f"**Username:** `{username}`")
            st.markdown(f"**Role:** {jabatan}")

        with col_right:
            st.subheader("Edit Informasi Akun")

            nama_baru = st.text_input(
                "Nama Lengkap",
                value=nama if nama else ""
            )

            jenis_kelamin_options = ["Laki-laki", "Perempuan"]

            jenis_kelamin_baru = st.selectbox(
                "Jenis Kelamin",
                jenis_kelamin_options,
                index=jenis_kelamin_options.index(jenis_kelamin)
                if jenis_kelamin in jenis_kelamin_options
                else 0
            )

            jabatan_options = [
                "Owner",
                "Manager",
                "Admin",
                "Kasir",
                "Barista",
                "Staff"
            ]

            jabatan_baru = st.selectbox(
                "Jabatan",
                jabatan_options,
                index=jabatan_options.index(jabatan)
                if jabatan in jabatan_options
                else 0
            )

            email_baru = st.text_input(
                "Email",
                value=email if email else ""
            )

            st.text_input(
                "Username",
                value=username,
                disabled=True
            )

            if st.button("💾 Simpan Perubahan Profile", use_container_width=True):

                foto_path = foto_profil

                if uploaded_file is not None:
                    foto_path = save_profile_photo(uploaded_file, username)

                update_user_profile(
                    nama_baru,
                    jenis_kelamin_baru,
                    jabatan_baru,
                    email_baru,
                    foto_path,
                    username
                )

                st.session_state.nama = nama_baru
                st.session_state.jabatan = jabatan_baru

                st.success("Profile berhasil diperbarui.")
                st.toast("✅ Profile berhasil diperbarui", icon="👤")
                st.rerun()

    with tab_security:

        st.subheader("🔑 Ganti Password")
        st.caption("Gunakan password yang kuat untuk menjaga keamanan akun.")

        st.markdown("""
        <div style="
            background:#EFF6FF;
            padding:14px;
            border-radius:12px;
            border-left:5px solid #1E5FD8;
            margin-bottom:18px;
            color:#1E293B;
        ">
        🔒 <b>Syarat Password Baru</b><br>
        • Minimal 8 karakter<br>
        • Mengandung minimal 1 huruf besar (A-Z)<br>
        • Mengandung minimal 1 angka (0-9)
        </div>
        """, unsafe_allow_html=True)

        old_password = st.text_input(
            "Password Lama",
            type="password",
            key="old_password"
        )

        new_password = st.text_input(
            "Password Baru",
            type="password",
            key="new_password"
        )

        confirm_new_password = st.text_input(
            "Konfirmasi Password Baru",
            type="password",
            key="confirm_new_password"
        )

        if st.button("🔐 Simpan Password Baru", use_container_width=True):

            if not old_password or not new_password or not confirm_new_password:
                st.warning("Semua field password wajib diisi.")

            elif len(new_password) < 8:
                st.error("Password baru minimal 8 karakter.")

            elif not any(char.isupper() for char in new_password):
                st.error("Password baru harus memiliki minimal 1 huruf besar.")

            elif not any(char.isdigit() for char in new_password):
                st.error("Password baru harus memiliki minimal 1 angka.")

            elif new_password != confirm_new_password:
                st.error("Konfirmasi password baru tidak sama.")

            else:
                success, message = change_password(
                    username,
                    old_password,
                    new_password
                )

                if success:
                    st.success(message)
                    st.toast("🔐 Password berhasil diubah", icon="✅")
                else:
                    st.error(message)