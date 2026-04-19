import json
from pathlib import Path

import requests

BASE_URL = "http://127.0.0.1:8010"
PROJECT_ID = 1

REPORT_PATH = Path("pytest_report.json")


def load_report() -> dict:
    if not REPORT_PATH.exists():
        raise FileNotFoundError(f"Report file not found: {REPORT_PATH}")

    with REPORT_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def create_test_run(report: dict) -> int:
    summary = report.get("summary", {})

    payload = {
        "project_id": PROJECT_ID,
        "run_name": "Pytest JSON Report Run",
        "source_type": "pytest",
        "source_name": "local-pytest-json-report",
        "external_run_id": str(report.get("created")),
        "status": "failed" if summary.get("failed", 0) > 0 else "passed",
        "total_tests": summary.get("total", 0),
        "passed_tests": summary.get("passed", 0),
        "failed_tests": summary.get("failed", 0),
    }

    response = requests.post(f"{BASE_URL}/test-runs/", json=payload, timeout=10)
    response.raise_for_status()

    data = response.json()
    return data["id"]


def parse_test_name(nodeid: str) -> str:
    return nodeid.split("::")[-1]


def parse_duration_ms(test: dict) -> int:
    call_data = test.get("call", {})
    duration_seconds = call_data.get("duration", 0)
    return int(duration_seconds * 1000)


def parse_error_message(test: dict) -> str | None:
    call_data = test.get("call", {})

    if call_data.get("outcome") != "failed":
        return None

    if "longrepr" in call_data:
        return call_data["longrepr"]

    crash = call_data.get("crash")
    if crash and "message" in crash:
        return crash["message"]

    return "Unknown test failure"


def upload_test_results(test_run_id: int, report: dict) -> None:
    tests = report.get("tests", [])

    for test in tests:
        payload = {
            "test_run_id": test_run_id,
            "test_name": parse_test_name(test["nodeid"]),
            "status": test.get("outcome", "unknown"),
            "duration_ms": parse_duration_ms(test),
            "error_message": parse_error_message(test),
        }

        response = requests.post(
            f"{BASE_URL}/test-results/",
            json=payload,
            timeout=10,
        )
        response.raise_for_status()


def main() -> None:
    report = load_report()
    test_run_id = create_test_run(report)
    upload_test_results(test_run_id, report)

    print(f"Uploaded pytest results into test_run_id={test_run_id}")


if __name__ == "__main__":
    main()