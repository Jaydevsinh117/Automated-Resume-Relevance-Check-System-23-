# student_app.py
import streamlit as st
import requests
import json
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api/v1")

st.set_page_config(
    page_title="Innomatics Resume Checker - Student Portal",
    page_icon="📄",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .score-high { color: #4CAF50; font-size: 2rem; font-weight: bold; }
    .score-medium { color: #FF9800; font-size: 2rem; font-weight: bold; }
    .score-low { color: #F44336; font-size: 2rem; font-weight: bold; }
    .verdict-box {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .verdict-high { background-color: #E8F5E9; border: 2px solid #4CAF50; }
    .verdict-medium { background-color: #FFF3E0; border: 2px solid #FF9800; }
    .verdict-low { background-color: #FFEBEE; border: 2px solid #F44336; }
    .card {
        background: white;
        padding: 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

class APIClient:
    def __init__(self):
        self.base_url = API_BASE_URL
        self.token = st.session_state.get('token', None)
    
    def get_headers(self):
        if self.token:
            return {"Authorization": f"Bearer {self.token}"}
        return {}
    
    def login(self, email, password):
        try:
            form_data = {
                "username": email,
                "password": password,
                "grant_type": "password"
            }
            response = requests.post(f"{self.base_url}/token", data=form_data)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            st.error(f"Login error: {str(e)}")
            return None
    
    def register(self, email, password, full_name, is_admin=False):
        try:
            data = {
                "email": email,
                "password": password,
                "full_name": full_name,
                "is_admin": is_admin
            }
            response = requests.post(f"{self.base_url}/register", json=data)
            return response.status_code == 200
        except Exception as e:
            st.error(f"Registration error: {str(e)}")
            return False
    
    def upload_file(self, file):
        try:
            files = {"file": (file.name, file.getvalue(), file.type)}
            headers = self.get_headers()
            response = requests.post(f"{self.base_url}/upload-file", files=files, headers=headers)
            return response.json() if response.status_code == 200 else None
        except Exception as e:
            st.error(f"Upload error: {str(e)}")
            return None
    
    def create_evaluation(self, evaluation_data):
        try:
            headers = self.get_headers()
            response = requests.post(f"{self.base_url}/evaluations", json=evaluation_data, headers=headers)
            return response.json() if response.status_code == 200 else None
        except Exception as e:
            st.error(f"Evaluation error: {str(e)}")
            return None
    
    def get_job_descriptions(self):
        try:
            headers = self.get_headers()
            response = requests.get(f"{self.base_url}/job-descriptions", headers=headers)
            return response.json() if response.status_code == 200 else []
        except Exception as e:
            st.error(f"Error fetching job descriptions: {str(e)}")
            return []
    
    def get_user_info(self):
        try:
            headers = self.get_headers()
            response = requests.get(f"{self.base_url}/me", headers=headers)
            return response.json() if response.status_code == 200 else None
        except Exception as e:
            st.error(f"Error fetching user info: {str(e)}")
            return None
    
    def get_user_evaluations(self):
        try:
            headers = self.get_headers()
            user_id = st.session_state.get('user_id')
            response = requests.get(f"{self.base_url}/users/{user_id}/evaluations", headers=headers)
            return response.json() if response.status_code == 200 else []
        except Exception as e:
            st.error(f"Error fetching evaluations: {str(e)}")
            return []

def login_page():
    st.markdown('<h1 class="main-header">📄 Innomatics Resume Relevance Checker</h1>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])
    
    with tab1:
        st.subheader("Login to Your Account")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login", type="primary", use_container_width=True):
            if email and password:
                api_client = APIClient()
                result = api_client.login(email, password)
                if result:
                    st.session_state.token = result['access_token']
                    st.session_state.user_id = result['user_id']
                    st.session_state.is_admin = result['is_admin']
                    st.session_state.user_email = email
                    st.success("Login successful!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Login failed. Check your credentials.")
    
    with tab2:
        st.subheader("Create New Account")
        full_name = st.text_input("Full Name", key="reg_name")
        email = st.text_input("Email", key="reg_email")
        password = st.text_input("Password", type="password", key="reg_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm")
        
        if st.button("Register", use_container_width=True):
            if all([full_name, email, password, confirm_password]):
                if password == confirm_password:
                    api_client = APIClient()
                    success = api_client.register(email, password, full_name)
                    if success:
                        st.success("Registration successful! Please login.")
                    else:
                        st.error("Registration failed. Email may already exist.")
                else:
                    st.error("Passwords do not match")

def main_app():
    api_client = APIClient()
    
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown('<h1 class="main-header">📄 Innomatics Resume Relevance Checker</h1>', unsafe_allow_html=True)
    with col2:
        if st.button("🚪 Logout", type="secondary"):
            for key in ['token', 'user_id', 'is_admin', 'user_email']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
    
    # Navigation
    tab1, tab2 = st.tabs(["🎯 New Evaluation", "📊 My Evaluations"])
    
    with tab1:
        st.header("🎯 New Resume Evaluation")
        
        # Initialize session state
        if 'jd_text' not in st.session_state:
            st.session_state.jd_text = ""
        if 'resume_text' not in st.session_state:
            st.session_state.resume_text = ""
        if 'results' not in st.session_state:
            st.session_state.results = None
        
        # Get job descriptions
        job_descriptions = api_client.get_job_descriptions()
        
        if not job_descriptions:
            st.warning("No job descriptions available. Please ask placement team to upload JDs.")
            return
        
        # Job description selection
        jd_options = {jd['id']: f"{jd['title']} - {jd['company']} ({jd.get('location', 'Remote')})" 
                     for jd in job_descriptions if jd['is_active']}
        
        if not jd_options:
            st.warning("No active job descriptions available.")
            return
        
        selected_jd = st.selectbox("📋 Select Job Description", options=list(jd_options.keys()), 
                                 format_func=lambda x: jd_options[x])
        
        # File upload section
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📄 Upload Resume")
            resume_file = st.file_uploader("Choose PDF/DOCX file", type=["pdf", "docx", "doc"], key="resume_upload")
            if resume_file and st.button("📝 Process Resume", key="process_resume"):
                with st.spinner("Extracting text from resume..."):
                    result = api_client.upload_file(resume_file)
                    if result:
                        st.session_state.resume_text = result['extracted_text']
                        st.success(f"✅ Resume processed! {result['word_count']} words extracted")
        
        with col2:
            st.subheader("📝 Manual Input")
            st.session_state.resume_text = st.text_area("Or paste resume text here", 
                                                      st.session_state.resume_text, height=150)
        
        # Display resume text
        if st.session_state.resume_text:
            with st.expander("👀 Preview Resume Text"):
                st.text(st.session_state.resume_text[:500] + "..." if len(st.session_state.resume_text) > 500 
                       else st.session_state.resume_text)
        
        # Evaluation button
        if st.session_state.resume_text and selected_jd:
            if st.button("🚀 Evaluate Resume", type="primary", use_container_width=True):
                with st.spinner("Analyzing your resume..."):
                    progress_bar = st.progress(0)
                    for i in range(100):
                        time.sleep(0.01)
                        progress_bar.progress(i + 1)
                    
                    evaluation_data = {
                        "resume_text": st.session_state.resume_text,
                        "resume_file_name": resume_file.name if resume_file else "manual_input.txt",
                        "job_description_id": selected_jd
                    }
                    
                    results = api_client.create_evaluation(evaluation_data)
                    if results:
                        st.session_state.results = results
                        st.session_state.selected_jd = selected_jd
                        st.success("✅ Evaluation complete!")
                        st.rerun()
        
        # Display results
        if st.session_state.get('results'):
            display_results(st.session_state.results)
    
    with tab2:
        st.header("📊 My Evaluation History")
        evaluations = api_client.get_user_evaluations()
        
        if evaluations:
            for eval in evaluations:
                with st.expander(f"Evaluation #{eval['id']} - Score: {eval['relevance_score']}% - {eval['verdict']}"):
                    display_evaluation_summary(eval)
        else:
            st.info("No evaluations yet. Submit your first resume for evaluation!")

def display_results(results):
    st.divider()
    st.header("📊 Evaluation Results")
    
    # Score and Verdict
    col1, col2, col3 = st.columns(3)
    
    with col1:
        score = results['relevance_score']
        score_color = "score-high" if score >= 70 else "score-medium" if score >= 40 else "score-low"
        st.markdown(f'<div class="{score_color}">{score:.1f}/100</div>', unsafe_allow_html=True)
        st.metric("Overall Score", f"{score:.1f}/100")
    
    with col2:
        verdict = results['verdict']
        verdict_class = "verdict-high" if verdict.lower() == "high" else "verdict-medium" if verdict.lower() == "medium" else "verdict-low"
        st.markdown(f'<div class="verdict-box {verdict_class}"><h3>{"✅" if verdict.lower() == "high" else "⚠️" if verdict.lower() == "medium" else "❌"} {verdict} Suitability</h3></div>', unsafe_allow_html=True)
    
    with col3:
        st.metric("Skills Match", f"{results['hard_match_score']:.1f}/100")
        st.metric("Relevance Score", f"{results['semantic_match_score']:.1f}/100")
    
    # Detailed analysis
    st.subheader("🔍 Detailed Analysis")
    
    tab1, tab2, tab3 = st.tabs(["❌ Missing Skills", "💡 Improvement Suggestions", "📈 Score Breakdown"])
    
    with tab1:
        if results['missing_skills']:
            st.write("**Skills required but missing from your resume:**")
            for skill in results['missing_skills']:
                st.write(f"• ❌ {skill}")
        else:
            st.success("🎉 Excellent! No critical skills missing!")
    
    with tab2:
        st.write("**Personalized improvement suggestions:**")
        for i, suggestion in enumerate(results['suggestions'], 1):
            st.write(f"{i}. 💡 {suggestion}")
    
    with tab3:
        st.write("**How your score was calculated:**")
        st.write(f"**Hard Skills Match (30%):** {results['hard_match_score']:.1f}%")
        st.write(f"**Semantic Relevance (70%):** {results['semantic_match_score']:.1f}%")
        st.write(f"**Final Score:** {results['relevance_score']:.1f}%")
        
        # Visual score breakdown
        score_data = {
            'Component': ['Hard Skills', 'Semantic Relevance'],
            'Score': [results['hard_match_score'], results['semantic_match_score']],
            'Weight': [30, 70]
        }
        st.bar_chart(score_data, x='Component', y=['Score', 'Weight'])
    
    # Download results
    st.divider()
    st.subheader("💾 Download Results")
    json_results = json.dumps(results, indent=2)
    st.download_button(
        label="📥 Download JSON Report",
        data=json_results,
        file_name="resume_evaluation_report.json",
        mime="application/json"
    )

def display_evaluation_summary(eval):
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Overall Score", f"{eval['relevance_score']:.1f}%")
        st.metric("Verdict", eval['verdict'])
        st.write(f"**Date:** {eval['created_at'][:10]}")
    
    with col2:
        st.metric("Skills Match", f"{eval['hard_match_score']:.1f}%")
        st.metric("Relevance", f"{eval['semantic_match_score']:.1f}%")
    
    if eval['missing_skills']:
        st.write("**Missing Skills:**")
        for skill in eval['missing_skills'][:3]:  # Show top 3
            st.write(f"• ❌ {skill}")

def main():
    if 'token' not in st.session_state:
        login_page()
    else:
        main_app()

if __name__ == "__main__":
    main()