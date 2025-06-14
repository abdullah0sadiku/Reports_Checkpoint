# Reports Checkpoint

## Overview

Reports Checkpoint is an Apache Airflow project designed to automate the daily verification of employee report submissions. It includes:

- **Airflow DAGs** for orchestrating report checks and notifications.
- **A FastAPI backend** for collecting and serving daily employee reports.
- Example ETL DAGs to demonstrate Airflow's TaskFlow API and dynamic task mapping.

---

## Project Structure

```
.
├── API/                # FastAPI backend for report submission
│   ├── [`API/API.py`](API/API.py )
│   └── reports/        # Saved report JSON files
├── dags/               # Airflow DAGs
│   ├── [`dags/check_dag.py`](dags/check_dag.py )    # Main report-checking DAG
│   └── [`dags/exampledag.py`](dags/exampledag.py )   # Example astronaut ETL DAG
├── tests/              # Pytest-based DAG tests
│   └── dags/
├── .astro/             # Astronomer config and DAG integrity tests
├── Dockerfile
├── [`requirements.txt`](requirements.txt )
├── [`packages.txt`](packages.txt )
└── [`README.md`](README.md )
```

---

## Features

- **Automated Report Checking:**  
  The [`report_check_dag`](dags/check_dag.py) Airflow DAG fetches daily reports from the FastAPI backend, checks for missing submissions, archives reports, and alerts HR if any are missing.

- **API for Report Submission:**  
  The FastAPI app ([`API.py`](API/API.py)) allows employees to submit daily reports and provides an endpoint for Airflow to fetch today's reports.

- **Example ETL DAG:**  
  The [`example_astronauts`](dags/exampledag.py) DAG demonstrates Airflow's TaskFlow API and dynamic task mapping.

- **Testing:**  
  Pytest-based tests in [`tests/dags/test_dag_example.py`](tests/dags/test_dag_example.py) ensure DAG integrity and enforce best practices.

---

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/)
- [Astronomer CLI](https://docs.astronomer.io/astro/cli/install-cli)

### Setup

1. **Clone the repository:**
   ```sh
   git clone <your-repo-url>
   cd <project-directory>
   ```

2. **Start Airflow locally:**
   ```sh
   astro dev start
   ```
   This will spin up Airflow and its dependencies in Docker containers.

3. **Run the FastAPI backend:**
   ```sh
   cd API
   uvicorn API:app --reload --host 0.0.0.0 --port 5000
   ```
   (You may need to install dependencies: `pip install fastapi uvicorn`)

4. **Access Airflow UI:**  
   Visit [http://localhost:8080](http://localhost:8080) in your browser.

---

## Usage

- **Submit a report:**  
  Send a POST request to `http://localhost:5000/upload` with JSON:
  ```json
  {
    "employee": "Your Name",
    "report": "Your daily report text"
  }
  ```

- **Check reports:**  
  The Airflow DAG [`report_check_dag`](dags/check_dag.py ) will fetch and verify reports daily, alerting HR if any are missing.

---

## Testing

Run all tests with:
```sh
pytest tests/
```

---

## Customization

- **Expected Employees:**  
  Edit the [`EXPECTED_EMPLOYEES`](dags/check_dag.py ) list in [`check_dag.py`](dags/check_dag.py ).

- **Archiving Logic:**  
  Implement your own archiving in the [`archive_reports`](dags/check_dag.py ) task in [`check_dag.py`](dags/check_dag.py ).

---

## Contact

For questions or support, contact the project maintainer.
