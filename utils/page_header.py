import streamlit as st


def show_page_header(icon, title, subtitle):
    st.markdown(
        f"""
        <div style="background:linear-gradient(135deg,#1E5FD8,#3B82F6);border-radius:22px;padding:30px 34px;margin-bottom:26px;box-shadow:0px 12px 28px rgba(30,95,216,0.25);">
            <h1 style="margin:0;color:white;font-size:34px;font-weight:900;">
                {icon} {title}
            </h1>
            <p style="margin-top:10px;margin-bottom:0;color:white;opacity:0.9;font-size:16px;line-height:1.5;">
                {subtitle}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )