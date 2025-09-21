# pages/Home.py
import streamlit as st
from components.api_client import APIClient

def show():
    st.markdown("<h1 style='text-align:center; color:#1E88E5;'>📄 Innomatics Resume Relevance System</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>AI-powered resume evaluation for better placement opportunities</p>", unsafe_allow_html=True)

    api = APIClient()

    # -----------------------
    # API Health
    # -----------------------
    st.subheader("⚡ System Health Check")
    health = api.health()
    if health.get("status") == "healthy":
        st.success("✅ Backend API is running")
    else:
        st.error(f"❌ API error: {health}")

    st.markdown("---")

    # -----------------------
    # Jobs Overview
    # -----------------------
    st.subheader("💼 Job Descriptions (from backend)")
    jobs = api.get_jobs()
    job_data = []
    if isinstance(jobs, dict) and jobs.get("status") == "success":
        job_data = jobs.get("data", [])
    elif isinstance(jobs, list):
        job_data = jobs

    if job_data:
        for job in job_data:
            with st.expander(f"{job.get('title')} @ {job.get('company', '')} (ID: {job['id']})"):
                st.json(job)
    else:
        st.info("No job descriptions found.")

    st.markdown("---")

    # -----------------------
    # Resumes Overview
    # -----------------------
    st.subheader("📄 Resumes (from backend)")
    resumes = api.get_resumes()
    resume_data = []
    if isinstance(resumes, dict) and resumes.get("status") == "success":
        resume_data = resumes.get("data", [])
    elif isinstance(resumes, list):
        resume_data = resumes

    if resume_data:
        for r in resume_data:
            with st.expander(f"{r.get('student_name')} ({r.get('email')}) - ID {r['id']}"):
                st.json(r)
    else:
        st.info("No resumes uploaded yet.")

    st.markdown("---")

    # -----------------------
    # Evaluations Overview
    # -----------------------
    st.subheader("🎯 Evaluations (from backend)")
    evaluations = api.get_evaluations()
    if evaluations:
        if isinstance(evaluations, dict):
            st.json(evaluations)
        elif isinstance(evaluations, list):
            for ev in evaluations:
                with st.expander(f"Evaluation ID {ev.get('id', '?')}"):
                    st.json(ev)
    else:
        st.info("No evaluations yet.")

    st.markdown("---")

    # -----------------------
    # Quick Navigation
    # -----------------------
    st.subheader("🔗 Quick Actions")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("👤 Student Portal"):
            st.session_state.current_page = "Student_Dashboard"
            st.experimental_rerun()

    with col2:
        if st.button("👑 Admin Portal"):
            st.session_state.current_page = "Admin_Dashboard"
            st.experimental_rerun()

    with col3:
        if st.button("ℹ️ Learn More"):
            st.info("""
            **Innomatics Resume System** helps students prepare better resumes and 
            enables placement teams to efficiently evaluate candidates against job requirements.
            
            Features:
            - AI-powered resume scoring
            - Skill gap analysis
            - Personalized suggestions
            - Placement team dashboard
            """)
