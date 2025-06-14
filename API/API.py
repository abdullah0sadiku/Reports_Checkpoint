from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import date, datetime
from typing import List
import os
import json

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development: allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory store for reports
daily_reports = {}

class Report(BaseModel):
    employee: str
    report: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the Daily Report API"}

@app.post("/upload")
def upload(report: Report):
    today = date.today().isoformat()
    now = datetime.now()
    timestamp = now.strftime("%H%M%S")
    employee_clean = report.employee.replace(" ", "_")
    filename = f"{today}_{employee_clean}_{timestamp}.json"
    reports_dir = "reports"
    os.makedirs(reports_dir, exist_ok=True)
    filepath = os.path.join(reports_dir, filename)

    # Save report as JSON
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump({
            "employee": report.employee,
            "report": report.report,
            "date": today,
            "timestamp": now.isoformat()
        }, f, ensure_ascii=False, indent=2)

    # (Optional) Still store in memory if you want
    if today not in daily_reports:
        daily_reports[today] = []
    daily_reports[today].append(report.dict())

    return {"message": "Report received", "file": filename}

@app.get("/reports/today")
def get_reports():
    today = date.today().isoformat()
    return {"reports": daily_reports.get(today, [])}
