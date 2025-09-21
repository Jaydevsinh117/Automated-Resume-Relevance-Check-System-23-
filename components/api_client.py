# components/api_client.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_BASE = os.getenv("API_BASE_URL", "http://localhost:8000")

class APIClient:
    def __init__(self):
        self.base = API_BASE.rstrip("/")

    # -----------------------
    # Health
    # -----------------------
    def health(self):
        try:
            r = requests.get(f"{self.base}/health", timeout=5)
            return r.json()
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # -----------------------
    # Jobs
    # -----------------------
    def create_job(self, payload: dict):
        return requests.post(f"{self.base}/jobs/jobs/", json=payload).json()

    def get_jobs(self):
        r = requests.get(f"{self.base}/jobs/jobs/")
        return r.json() if r.ok else []

    def get_job(self, job_id: int):
        r = requests.get(f"{self.base}/jobs/jobs/{job_id}")
        return r.json()

    def update_job(self, job_id: int, payload: dict):
        r = requests.put(f"{self.base}/jobs/jobs/{job_id}", json=payload)
        return r.json()

    def delete_job(self, job_id: int):
        r = requests.delete(f"{self.base}/jobs/jobs/{job_id}")
        return r.json()

    # -----------------------
    # Resumes
    # -----------------------
    def create_resume(self, payload: dict):
        r = requests.post(f"{self.base}/resumes/resumes/", json=payload)
        return r.json()

    def get_resumes(self):
        r = requests.get(f"{self.base}/resumes/resumes/")
        return r.json() if r.ok else []

    def get_resume(self, resume_id: int):
        r = requests.get(f"{self.base}/resumes/resumes/{resume_id}")
        return r.json()

    def update_resume(self, resume_id: int, payload: dict):
        r = requests.put(f"{self.base}/resumes/resumes/{resume_id}", json=payload)
        return r.json()

    def delete_resume(self, resume_id: int):
        r = requests.delete(f"{self.base}/resumes/resumes/{resume_id}")
        return r.json()

    def parse_resume(self, resume_id: int):
        r = requests.post(f"{self.base}/resumes/resumes/{resume_id}/parse")
        return r.json()

    # -----------------------
    # Evaluations
    # -----------------------
    def evaluate(self, resume_id: int, job_id: int):
        # backend expects form data
        data = {"resume_id": resume_id, "job_id": job_id}
        r = requests.post(f"{self.base}/evaluations/evaluation/", data=data)
        return r.json() if r.ok else {"status": "error", "message": r.text}

    def get_evaluations(self):
        r = requests.get(f"{self.base}/evaluations")
        return r.json() if r.ok else []
