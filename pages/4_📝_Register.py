# pages/4_📝_Register.py
import streamlit as st
from components.auth import AuthClient

def show():
    st.markdown('<h2 class="main-header">📝 Create Account</h2>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["🎯 Student Account", "👑 Placement Team Account"])

    # --------------------------
    # Student Registration
    # --------------------------
    with tab1:
        st.info("Create a student account to evaluate your resume against job descriptions")

        with st.form("student_reg_form"):
            full_name = st.text_input("👤 Full Name", placeholder="John Doe")
            email = st.text_input("📧 Email Address", placeholder="student@innomatics.com")
            password = st.text_input("🔒 Password", type="password", placeholder="Create a strong password")
            confirm_password = st.text_input("✅ Confirm Password", type="password", placeholder="Re-enter password")

            col1, col2 = st.columns(2)
            with col1:
                register_btn = st.form_submit_button("🎯 Create Student Account", use_container_width=True)
            with col2:
                if st.form_submit_button("⬅️ Back to Login", use_container_width=True):
                    st.session_state.current_page = "User_Login"
                    st.experimental_rerun()

        if register_btn:
            handle_registration(full_name, email, password, confirm_password, is_admin=False)

    # --------------------------
    # Admin Registration
    # --------------------------
    with tab2:
        st.warning("⚠️ Placement team accounts require admin approval. Contact IT department for access.")

        with st.form("admin_reg_form"):
            full_name = st.text_input("👤 Full Name (Admin)", placeholder="Jane Smith")
            email = st.text_input("📧 Work Email", placeholder="admin@innomatics.com")
            password = st.text_input("🔒 Password", type="password")
            confirm_password = st.text_input("✅ Confirm Password", type="password")
            admin_code = st.text_input("🔑 Admin Access Code", placeholder="Contact IT for access code")

            col1, col2 = st.columns(2)
            with col1:
                admin_reg_btn = st.form_submit_button("👑 Request Admin Access", use_container_width=True, disabled=True)
            with col2:
                if st.form_submit_button("⬅️ Back to Login", use_container_width=True):
                    st.session_state.current_page = "Admin_Login"
                    st.experimental_rerun()

        st.info("ℹ️ For placement team access, please contact your system administrator.")


# --------------------------
# Helper Function
# --------------------------
def handle_registration(full_name, email, password, confirm_password, is_admin):
    if not all([full_name, email, password, confirm_password]):
        st.error("⚠️ Please fill in all fields")
        return

    if password != confirm_password:
        st.error("⚠️ Passwords do not match")
        return

    if len(password) < 6:
        st.error("⚠️ Password must be at least 6 characters")
        return

    auth_client = AuthClient()
    success = auth_client.register({
        "email": email,
        "password": password,
        "full_name": full_name,
        "is_admin": is_admin
    })

    if success:
        st.success("✅ Account created successfully! Please login.")
        st.session_state.current_page = "User_Login"
        st.experimental_rerun()
    else:
        st.error("❌ Registration failed. Email may already exist.")
