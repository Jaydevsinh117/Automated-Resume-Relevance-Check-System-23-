# components/auth.py
import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
API_BASE = os.getenv("API_BASE_URL", "http://localhost:8000")

class AuthClient:
    def __init__(self):
        self.base = API_BASE.rstrip("/")

    # -----------------------
    # Login
    # -----------------------
    def login(self, email, password):
        try:
            form_data = {
                "username": email,
                "password": password,
                "grant_type": "password"
            }
            response = requests.post(f"{self.base}/auth/token", data=form_data)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            st.error(f"Login error: {str(e)}")
            return None

    # -----------------------
    # Register
    # -----------------------
    def register(self, user_data):
        try:
            response = requests.post(f"{self.base}/auth/register", json=user_data)
            return response.status_code == 200
        except Exception as e:
            st.error(f"Registration error: {str(e)}")
            return False

    # -----------------------
    # Forgot password
    # -----------------------
    def reset_password(self, email):
        try:
            response = requests.post(f"{self.base}/auth/forgot-password", json={"email": email})
            return response.status_code == 200
        except Exception as e:
            st.error(f"Password reset error: {str(e)}")
            return False
