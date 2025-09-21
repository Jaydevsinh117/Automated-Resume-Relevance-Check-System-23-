# dashboard_app.py
import os
import time
import requests
import streamlit as st
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv

# -----------------------
# Config
# -----------------------
load_dotenv()
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api/v1")

st.set_page_config(
    page_title="Innomatics - Placement Dashboard",
    page_icon="📊",
    layout="wide"
)

# -----------------------
# Custom CSS
# -----------------------
st.markdown("""
<style>
    .dashboard-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 1rem;
        color: white;
        margin-bottom: 2rem;
        text-align: center;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        text-align: center;
    }
    .filter-section {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 1rem;
        margin-bottom: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------
# API Client
# -----------------------
class DashboardAPI:
    def __init__(self):
        self.base_url = API_BASE_URL
        self.token = st.session_state.get("admin_token")

    def _headers(self):
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def _handle(self, response):
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            st.error("⚠️ Session expired. Please log in again.")
            st.session_state.clear()
            st.rerun()
        else:
            st.error(f"API Error {response.status_code}: {response.text}")
        return None

    # Auth
    def login(self, email, password):
        form_data = {"username": email, "password": password, "grant_type": "password"}
        r = requests.post(f"{self.base_url}/token", data=form_data)
        return self._handle(r)

    # Users
    def get_all_users(self):
        r = requests.get(f"{self.base_url}/admin/users", headers=self._headers())
        return self._handle(r) or []

    # Evaluations
    def get_evaluations(self, filters=None):
        r = requests.get(f"{self.base_url}/admin/evaluations", headers=self._headers(), params=filters or {})
        return self._handle(r) or []

    # Jobs
    def get_job_descriptions(self, active_only=False):
        params = {"active_only": active_only} if active_only else {}
        r = requests.get(f"{self.base_url}/admin/job-descriptions", headers=self._headers(), params=params)
        return self._handle(r) or []

    def create_job_description(self, jd_data):
        r = requests.post(f"{self.base_url}/admin/job-descriptions", headers=self._headers(), json=jd_data)
        return self._handle(r)

# -----------------------
# UI Helpers
# -----------------------
def metric_card(title, value, icon):
    return f'<div class="metric-card"><h3>{icon} {title}</h3><h2>{value}</h2></div>'

# -----------------------
# Pages
# -----------------------
def admin_login_page(api: DashboardAPI):
    st.markdown("""
    <div class="dashboard-header">
        <h1>📊 Innomatics Placement Team Dashboard</h1>
        <p>Admin Login Required</p>
    </div>
    """, unsafe_allow_html=True)

    email = st.text_input("Admin Email", key="admin_email")
    password = st.text_input("Password", type="password", key="admin_password")

    if st.button("Login as Admin", type="primary", use_container_width=True):
        result = api.login(email, password)
        if result and result.get("is_admin", False):
            st.session_state.admin_token = result["access_token"]
            st.session_state.admin_user_id = result["user_id"]
            st.session_state.admin_email = email
            st.success("✅ Login successful!")
            time.sleep(1)
            st.rerun()
        else:
            st.error("❌ Invalid admin credentials")

def overview_tab(api: DashboardAPI):
    users = api.get_all_users()
    evaluations = api.get_evaluations()
    jobs = api.get_job_descriptions()

    col1, col2, col3, col4 = st.columns(4)
    metrics = [
        ("Total Users", len(users), "👥"),
        ("Evaluations", len(evaluations), "📊"),
        ("Active Jobs", len([j for j in jobs if j.get("is_active")]), "💼"),
        ("Avg Score", f"{sum(e['relevance_score'] for e in evaluations)/len(evaluations):.1f}" if evaluations else "0", "⭐")
    ]
    for i, (title, value, icon) in enumerate(metrics):
        with [col1, col2, col3, col4][i]:
            st.markdown(metric_card(title, value, icon), unsafe_allow_html=True)

    if evaluations:
        col1, col2 = st.columns(2)
        with col1:
            scores = [e["relevance_score"] for e in evaluations]
            st.plotly_chart(px.histogram(x=scores, nbins=10, title="Score Distribution"), use_container_width=True)
        with col2:
            verdicts = [e["verdict"] for e in evaluations]
            st.plotly_chart(px.pie(values=pd.Series(verdicts).value_counts().values,
                                   names=pd.Series(verdicts).value_counts().index,
                                   title="Verdict Distribution"),
                            use_container_width=True)

def candidates_tab(api: DashboardAPI):
    st.header("👥 Candidate Management")

    col1, col2, col3 = st.columns(3)
    min_score = col1.slider("Min Score", 0, 100, 0)
    max_score = col2.slider("Max Score", 0, 100, 100)
    verdict_filter = col3.selectbox("Verdict", ["All", "High", "Medium", "Low"])

    filters = {}
    if min_score > 0: filters["min_score"] = min_score
    if max_score < 100: filters["max_score"] = max_score
    if verdict_filter != "All": filters["verdict"] = verdict_filter

    evaluations = api.get_evaluations(filters)

    if evaluations:
        df = pd.DataFrame(evaluations)
        st.dataframe(df[["id", "user_id", "relevance_score", "verdict", "created_at"]],
                     use_container_width=True, height=400)
    else:
        st.info("No evaluations match filters.")

def jobs_tab(api: DashboardAPI):
    st.header("💼 Job Description Management")

    with st.form("jd_form"):
        title = st.text_input("Job Title*")
        company = st.text_input("Company*")
        location = st.text_input("Location")
        skills = st.text_area("Required Skills (comma-separated)")
        description = st.text_area("Job Description*", height=100)
        if st.form_submit_button("Create Job"):
            if title and company and description:
                jd_data = {
                    "title": title,
                    "company": company,
                    "location": location,
                    "description_text": description,
                    "required_skills": [s.strip() for s in skills.split(",") if s.strip()]
                }
                if api.create_job_description(jd_data):
                    st.success("✅ Job created")
                else:
                    st.error("❌ Failed to create job")
            else:
                st.error("⚠️ Required fields missing")

    st.subheader("Existing Jobs")
    jobs = api.get_job_descriptions()
    for jd in jobs:
        with st.expander(f"{jd['title']} - {jd['company']}"):
            st.write(jd)

def settings_tab():
    st.header("⚙️ System Settings")
    st.info("Placement team features coming soon...")
    st.write("• User management")
    st.write("• Analytics & reports")
    st.write("• Export data")
    st.write("• Notifications")

# -----------------------
# App Entrypoint
# -----------------------
def main():
    api = DashboardAPI()

    if not st.session_state.get("admin_token"):
        admin_login_page(api)
    else:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("""
            <div class="dashboard-header">
                <h1>📊 Innomatics Placement Team Dashboard</h1>
                <p>Manage jobs and evaluations</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            if st.button("🚪 Logout", type="secondary"):
                st.session_state.clear()
                st.rerun()

        tab1, tab2, tab3, tab4 = st.tabs(["📈 Overview", "👥 Candidates", "💼 Jobs", "⚙️ Settings"])
        with tab1: overview_tab(api)
        with tab2: candidates_tab(api)
        with tab3: jobs_tab(api)
        with tab4: settings_tab()

if __name__ == "__main__":
    main()
