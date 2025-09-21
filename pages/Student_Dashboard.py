# pages/Student_Dashboard.py
import streamlit as st
import pandas as pd
from components.api_client import APIClient

def show():
    api = APIClient()
    st.markdown("<h2 style='color:#1E88E5;'>🎯 Student Dashboard</h2>", unsafe_allow_html=True)

    # Ensure session user
    if not st.session_state.get("user_info"):
        st.warning("⚠️ Please login first")
        st.session_state.current_page = "User_Login"
        st.experimental_rerun()
        return

    # -----------------------
    # RESUME SECTION
    # -----------------------
    st.subheader("📄 My Resume")

    with st.expander("➕ Create Resume Entry"):
        name = st.text_input("Name", value=st.session_state.user_info.get("email", ""))
        email = st.text_input("Email", value=st.session_state.user_info.get("email", ""))
        file_path = st.text_input("File Path (optional, local placeholder)")
        if st.button("Save Resume Entry"):
            payload = {
                "student_name": name,
                "email": email,
                "file_path": file_path,
                "skills": [],
                "education": [],
                "experience": []
            }
            res = api.create_resume(payload)
            st.json(res)
            if res.get("status") == "success":
                st.session_state.latest_resume_id = res["data"]["id"]

    # Show existing resumes
    resumes_resp = api.get_resumes()
    resumes = []
    if isinstance(resumes_resp, dict) and resumes_resp.get("status") == "success":
        resumes = resumes_resp.get("data", [])
    elif isinstance(resumes_resp, list):
        resumes = resumes_resp

    if resumes:
        df = pd.DataFrame(resumes)
        st.dataframe(df)
        rid = st.selectbox("Select Resume ID", options=[r["id"] for r in resumes])
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📝 Parse Resume"):
                st.json(api.parse_resume(int(rid)))
        with col2:
            if st.button("🗑 Delete Resume"):
                st.json(api.delete_resume(int(rid)))
    else:
        st.info("No resumes found. Create one above.")

    st.markdown("---")

    # -----------------------
    # JOB SECTION
    # -----------------------
    st.subheader("💼 Job Descriptions")

    jobs_resp = api.get_jobs()
    jobs = []
    if isinstance(jobs_resp, dict) and jobs_resp.get("status") == "success":
        jobs = jobs_resp.get("data", [])
    elif isinstance(jobs_resp, list):
        jobs = jobs_resp

    job_id = None
    if jobs:
        job_map = {j["id"]: f"{j['title']} @ {j.get('company','')}" for j in jobs}
        job_id = st.selectbox("Select Job", options=list(job_map.keys()), format_func=lambda x: job_map[x])
    else:
        st.info("No jobs available yet. Create one below.")

    with st.expander("➕ Create Job Description"):
        title = st.text_input("Job Title")
        company = st.text_input("Company")
        location = st.text_input("Location")
        description = st.text_area("Job Description")
        if st.button("Save Job Description"):
            payload = {
                "title": title,
                "company": company,
                "location": location,
                "description": description,
                "must_have_skills": [],
                "good_to_have_skills": [],
                "keywords": []
            }
            jr = api.create_job(payload)
            st.json(jr)
            if jr.get("status") == "success":
                job_id = jr["data"]["id"]

    st.markdown("---")

    # -----------------------
    # EVALUATION SECTION
    # -----------------------
    st.subheader("🎯 Resume Evaluation")

    if resumes and job_id:
        if st.button("🚀 Run Evaluation"):
            result = api.evaluate(rid, job_id)
            st.json(result)
            if result.get("status") == "success":
                st.success(f"✅ Score: {result['data']['score']} | Verdict: {result['data']['verdict']}")
                st.session_state.last_eval = result
    else:
        st.warning("Please create/select both a resume and a job before evaluation.")

    st.markdown("---")

    # -----------------------
    # HISTORY SECTION
    # -----------------------
    st.subheader("📊 Evaluation History")
    evs = api.get_evaluations()
    if evs:
        if isinstance(evs, dict):
            st.json(evs)
        elif isinstance(evs, list) and len(evs) > 0:
            df_evs = pd.DataFrame(evs)
            st.dataframe(df_evs)
        else:
            st.info("No evaluation results yet.")
    else:
        st.info("No evaluations found in system.")
