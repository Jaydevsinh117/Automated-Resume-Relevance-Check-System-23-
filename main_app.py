# main_app.py
import os
import importlib
import streamlit as st
from dotenv import load_dotenv
from components.api_client import APIClient

load_dotenv()

# -----------------------
# Initialize Session State
# -----------------------
DEFAULT_PAGE = "Home"

if "current_page" not in st.session_state:
    st.session_state.current_page = DEFAULT_PAGE
if "token" not in st.session_state:
    st.session_state.token = None
if "user_info" not in st.session_state:
    st.session_state.user_info = {}

# -----------------------
# Sidebar Navigation
# -----------------------
st.sidebar.title("📌 Navigation")

# Page map (keys = file names, values = display titles)
pages = {
    "Home": "🏠 Home",
    "User_Login": "👤 Student Login",
    "Admin_Login": "👑 Admin Login",
    "Register": "📝 Register",
    "Forgot_Password": "🔐 Forgot Password",
    "Student_Dashboard": "🎯 Student Dashboard",
    "Admin_Dashboard": "📊 Admin Dashboard",
}

# Radio selection
choice = st.sidebar.radio("Go to", list(pages.keys()), format_func=lambda k: pages[k])

# Navigation button
if st.sidebar.button("➡️ Go"):
    st.session_state.current_page = choice
    st.experimental_rerun()

# -----------------------
# User Info / Session
# -----------------------
if st.session_state.token:
    user = st.session_state.get("user_info", {})
    st.sidebar.markdown("---")
    st.sidebar.success(f"✅ Logged in as **{user.get('email', 'Unknown')}**")
    if st.sidebar.button("🚪 Logout"):
        st.session_state.token = None
        st.session_state.user_info = {}
        st.session_state.current_page = DEFAULT_PAGE
        st.experimental_rerun()
else:
    st.sidebar.info("Not logged in")

# -----------------------
# Health Check
# -----------------------
st.sidebar.markdown("---")
api = APIClient()
health = api.health()
if health.get("status") == "healthy":
    st.sidebar.success("API: ✅ Online")
else:
    st.sidebar.error("API: ❌ Offline")

# -----------------------
# Load Selected Page
# -----------------------
try:
    module = importlib.import_module(f"pages.{st.session_state.current_page}")
    module.show()
except Exception as e:
    st.error(f"⚠️ Page error: {e}")
    st.session_state.current_page = DEFAULT_PAGE
    st.experimental_rerun()
