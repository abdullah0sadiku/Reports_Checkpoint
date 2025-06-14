from airflow.decorators import dag, task
from pendulum import datetime
import requests

EXPECTED_EMPLOYEES = ["Abdulla", "Erina", "Graniti", "Kanita"]

@dag(
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["report-check"],
    default_args={"owner": "report_checker", "retries": 1},
)
def report_check_dag():
    """
    DAG to check daily employee reports and alert if any are missing.
    """

    @task()
    def fetch_reports():
        url = "http://host.docker.internal:5000/reports/today"
        try:
            response = requests.get(url)
            response.raise_for_status()
            reports = response.json().get("reports", [])
            return reports
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to fetch reports: {e}")

    @task()
    def check_reports(reports):
        submitted_employees = {r.get("employee") for r in reports}
        missing_employees = [e for e in EXPECTED_EMPLOYEES if e not in submitted_employees]

        if missing_employees:
            alert_msg = f"⚠️ Missing reports from: {', '.join(missing_employees)}"
            print(alert_msg)
            return {"status": "missing_reports", "missing": missing_employees}
        else:
            print("✅ All reports submitted.")
            return {"status": "all_reports_present"}

    @task()
    def archive_reports(reports):
        print(f"Archiving {len(reports)} reports...")
        # Placeholder for archiving logic
        return "archived"

    @task()
    def alert_hr(check_result):
        if check_result["status"] == "missing_reports":
            missing = check_result["missing"]
            print(f"🚨 HR ALERT: Missing reports from: {', '.join(missing)}")
        else:
            print("📩 HR INFO: All employees submitted reports.")

    # DAG Dependencies
    fetch = fetch_reports()
    check = check_reports(fetch)
    archive = archive_reports(fetch)

    # Wait for both check and archive to finish before alerting HR
    alert = alert_hr(check)

    [check, archive] >> alert

dag = report_check_dag()
