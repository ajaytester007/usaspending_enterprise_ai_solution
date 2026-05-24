import json
import time
from pathlib import Path
from typing import Iterable, Dict, Any
import requests

ENDPOINT = "https://api.usaspending.gov/api/v2/search/spending_over_time/"

QUARTERS = [
    ("Q1", "01-01", "03-31"),
    ("Q2", "04-01", "06-30"),
    ("Q3", "07-01", "09-30"),
    ("Q4", "10-01", "12-31"),
]

DEFAULT_AWARD_TYPES = ["A", "B", "C", "D", "02", "03", "04", "05"]


def build_body(state: str, start_date: str, end_date: str) -> Dict[str, Any]:
    return {
        "group": "quarter",
        "subawards": False,
        "filters": {
            "time_period": [{"start_date": start_date, "end_date": end_date}],
            "place_of_performance_scope": "domestic",
            "place_of_performance_locations": [{"country": "USA", "state": state}],
            "award_type_codes": DEFAULT_AWARD_TYPES,
        },
    }


def fetch_quarter(state: str, year: int, quarter: str, start_suffix: str, end_suffix: str) -> Dict[str, Any]:
    start_date = f"{year}-{start_suffix}"
    end_date = f"{year}-{end_suffix}"
    body = build_body(state, start_date, end_date)
    response = requests.post(ENDPOINT, json=body, timeout=90)
    response.raise_for_status()
    return {
        "source": "USAspending.gov",
        "endpoint": ENDPOINT,
        "state": state,
        "year": year,
        "quarter": quarter,
        "period_start": start_date,
        "period_end": end_date,
        "request": body,
        "response": response.json(),
        "fetched_at_epoch": time.time(),
    }


def fetch_range(states: Iterable[str], start_year: int, end_year: int, output_dir: str = "data/bronze/usaspending_spending_over_time") -> None:
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    for year in range(start_year, end_year + 1):
        for quarter, start_suffix, end_suffix in QUARTERS:
            for state in states:
                out_file = out_dir / f"state={state}_year={year}_quarter={quarter}.json"
                try:
                    payload = fetch_quarter(state, year, quarter, start_suffix, end_suffix)
                    out_file.write_text(json.dumps(payload, indent=2), encoding="utf-8")
                    print(f"BRONZE OK {out_file}")
                    time.sleep(0.15)
                except Exception as exc:
                    err_file = out_dir / f"ERROR_state={state}_year={year}_quarter={quarter}.json"
                    err_file.write_text(json.dumps({"state": state, "year": year, "quarter": quarter, "error": str(exc)}, indent=2), encoding="utf-8")
                    print(f"BRONZE FAIL {state} {year} {quarter}: {exc}")
