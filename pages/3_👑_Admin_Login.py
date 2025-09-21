# pages/3_👑_Admin_Login.py
import streamlit as st
from components.auth import AuthClient

def show():
    st.markdown('<h2 class="main-header">👑 Placement Team Login</h2>', unsafe_allow_html=True)
    st.warning("⚠️ This portal is for placement team members only. Students should use the Student Login.")

    with st.form("admin_login_form"):
        email = st.text_input("📧 Admin Email", placeholder="admin@innomatics.com")
        password = st.text_input("🔒 Password", type="password", placeholder="Enter admin password")

        col1, col2 = st.columns(2)
        with col1:
            login_btn = st.form_submit_button("👑 Admin Login", use_container_width=True)
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

        if result and result.get("is_admin", False):
            st.session_state.token = result["access_token"]
            st.session_state.user_info = {
                "id": result["user_id"],
                "email": email,
                "is_admin": True
            }
            st.session_state.user_type = "admin"
            st.success("✅ Admin login successful! Redirecting...")
            st.session_state.current_page = "Admin_Dashboard"
            st.experimental_rerun()
        else:
            st.error("❌ Admin access denied. Check credentials or contact system administrator.")

    # --------------------------
    # Info section
    # --------------------------
    with st.expander("ℹ️ Admin Information"):
        st.info("""
        **Placement Team Access Includes:**
        - Manage job descriptions
        - Review candidate evaluations
        - Access analytics and reports
        - System administration

        **Contact Support:** 
        - Admin account setup → IT department  
        - Placement queries → placement@innomatics.com
        """)
