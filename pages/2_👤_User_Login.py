# pages/2_👤_User_Login.py
import streamlit as st
from components.auth import AuthClient

def show():
    st.markdown('<h2 class="main-header">👤 Student Login</h2>', unsafe_allow_html=True)

    with st.form("user_login_form"):
        email = st.text_input("📧 Email Address", placeholder="student@innomatics.com")
        password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")

        col1, col2 = st.columns(2)
        with col1:
            login_btn = st.form_submit_button("🎯 Login", use_container_width=True)
        with col2:
            if st.form_submit_button("⬅️ Back to Home", use_container_width=True):
                st.session_state.current_page = "Home"
                st.experimental_rerun()

    if login_btn:
        if not email or not password:
            st.error("⚠️ Please fill in all fields")
            return

        auth_client = AuthClient()
        result = auth_client.login(email, password)

        if result:
            st.session_state.token = result["access_token"]
            st.session_state.user_info = {
                "id": result["user_id"],
                "email": email,
                "is_admin": result.get("is_admin", False)
            }
            st.session_state.user_type = "admin" if result.get("is_admin", False) else "user"

            if result.get("is_admin", False):
                st.success("✅ Logged in as Admin — redirecting...")
                st.session_state.current_page = "Admin_Dashboard"
            else:
                st.success("✅ Login successful! Redirecting...")
                st.session_state.current_page = "Student_Dashboard"

            st.experimental_rerun()
        else:
            st.error("❌ Login failed. Please check your credentials.")

    # --------------------------
    # Extra options
    # --------------------------
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📝 Create New Account", use_container_width=True):
            st.session_state.current_page = "Register"
            st.experimental_rerun()
    with col2:
        if st.button("🔐 Forgot Password", use_container_width=True):
            st.session_state.current_page = "Forgot_Password"
            st.experimental_rerun()
