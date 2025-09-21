# pages/Admin_Dashboard.py
import streamlit as st
import pandas as pd
from components.api_client import APIClient

def show():
    api = APIClient()
    st.markdown("<h2 style='color:#1E88E5;'>📊 Placement Team Dashboard</h2>", unsafe_allow_html=True)
    st.info("Manage job descriptions, resumes, and evaluation results.")

    # -----------------------
    # JOB MANAGEMENT
    # -----------------------
    st.subheader("💼 Manage Job Descriptions")

    # Create new job
    with st.expander("➕ Create New Job"):
        title = st.text_input("Job Title")
        company = st.text_input("Company")
        location = st.text_input("Location")
        description = st.text_area("Job Description")
        if st.button("Create Job"):
            payload = {
                "title": title,
                "company": company,
                "location": location,
                "description": description,
                "must_have_skills": [],
                "good_to_have_skills": [],
                "keywords": []
            }
            result = api.create_job(payload)
            st.write(result)

    # List jobs
    jobs_resp = api.get_jobs()
    jobs = []
    if isinstance(jobs_resp, dict) and jobs_resp.get("status") == "success":
        jobs = jobs_resp.get("data", [])
    elif isinstance(jobs_resp, list):
        jobs = jobs_resp

    if jobs:
        st.dataframe(pd.DataFrame(jobs))
        job_id = st.number_input("Job ID", step=1, min_value=1)
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🔎 Get Job by ID"):
                st.json(api.get_job(int(job_id)))
        with col2:
            if st.button("🗑 Delete Job"):
                st.json(api.delete_job(int(job_id)))
        with col3:
            new_title = st.text_input("New Title (for update)")
            if st.button("✏️ Update Job"):
                update_data = {"title": new_title}
                st.json(api.create_job(update_data))  # backend update not yet in api_client
    else:
        st.info("No jobs found.")

    st.markdown("---")

    # -----------------------
    # RESUME MANAGEMENT
    # -----------------------
    st.subheader("📄 Manage Resumes")

    with st.expander("➕ Create Resume"):
        student_name = st.text_input("Student Name")
        email = st.text_input("Email")
        file_path = st.text_input("File Path (local path or placeholder)")
        if st.button("Create Resume"):
            payload = {
                "student_name": student_name,
                "email": email,
                "file_path": file_path,
                "skills": [],
                "education": [],
                "experience": []
            }
            st.json(api.create_resume(payload))

    resumes_resp = api.get_resumes()
    resumes = []
    if isinstance(resumes_resp, dict) and resumes_resp.get("status") == "success":
        resumes = resumes_resp.get("data", [])
    elif isinstance(resumes_resp, list):
        resumes = resumes_resp

    if resumes:
        st.dataframe(pd.DataFrame(resumes))
        rid = st.number_input("Resume ID", step=1, min_value=1)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📝 Parse Resume"):
                st.json(api.parse_resume(int(rid)))
        with col2:
            if st.button("🗑 Delete Resume"):
                st.json(api.delete_resume(int(rid)))
    else:
        st.info("No resumes found.")

    st.markdown("---")

    # -----------------------
    # EVALUATIONS
    # -----------------------
    st.subheader("🎯 Evaluation Results")
    evs = api.get_evaluations()
    if evs:
        if isinstance(evs, dict):
            st.json(evs)
        elif isinstance(evs, list):
            df = pd.DataFrame(evs)
            st.dataframe(df)
    else:
        st.info("No evaluations available.")

    st.markdown("---")

    st.success("✅ Admin Dashboard loaded successfully")
