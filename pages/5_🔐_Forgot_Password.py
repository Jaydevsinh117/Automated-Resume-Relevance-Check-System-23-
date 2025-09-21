# pages/5_🔐_Forgot_Password.py
import streamlit as st
import re
from components.auth import AuthClient

def show():
    st.markdown('<h2 class="main-header">🔐 Password Recovery</h2>', unsafe_allow_html=True)
    
    api = AuthClient()

    tab1, tab2 = st.tabs(["📧 Email Recovery", "🆔 Security Questions"])
    
    # --------------------------
    # Email-based password reset
    # --------------------------
    with tab1:
        st.info("Enter your registered email to receive password reset instructions")
        email = st.text_input("📧 Email Address", placeholder="student@innomatics.com")
        
        if st.button("📨 Send Reset Link", use_container_width=True):
            if email and re.match(r"[^@]+@[^@]+\.[^@]+", email):
                success = api.reset_password(email)
                if success:
                    st.success(f"Password reset instructions sent to **{email}**")
                    st.info("Check your email inbox for the reset link. If not found, check spam/junk.")
                else:
                    st.error("Failed to send reset link. Please try again later.")
            else:
                st.error("⚠️ Please enter a valid email address")
    
    # --------------------------
    # Security questions (future)
    # --------------------------
    with tab2:
        st.info("Answer security questions to reset your password")
        st.warning("⚠️ Security question recovery not yet available.")
        st.text_input("What was your first pet's name?", disabled=True)
        st.text_input("What city were you born in?", disabled=True)
        st.button("Verify Answers", disabled=True)
    
    # --------------------------
    # Navigation
    # --------------------------
    st.markdown("---")
    if st.button("⬅️ Back to Login", use_container_width=True):
        st.session_state.current_page = "User_Login"
        st.experimental_rerun()
    
    # --------------------------
    # Contact Info
    # --------------------------
    with st.expander("📞 Need Help?"):
        st.info("""
        **Contact Support:**
        - Email: support@innomatics.com
        - Phone: +91-XXX-XXXX-XXXX
        - Office Hours: 9 AM - 6 PM (Mon-Fri)
        
        **Immediate help:**
        - Visit IT help desk
        - Contact your program coordinator
        """)
