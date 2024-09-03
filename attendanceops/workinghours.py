import json
from typing import Any, Dict, List

import openpyxl

# Constants
WORKER_HOURS_JSON_PATH = "workershours.json"
WORKER_DETAILS_JSON_PATH = "id2worker.json"
MONTHLY_ATTENDANCE_REPORT_XLS_PATH = "report_example.xlsx"


def load_json(file_path: str) -> Any:
    """Load JSON data from a file."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading JSON file {file_path}: {e}")
        return {}


def get_working_hours(file_path: str = WORKER_HOURS_JSON_PATH) -> Any:
    """Get working hours from a JSON file."""
    return load_json(file_path)


def get_worker_data(file_path: str = WORKER_DETAILS_JSON_PATH) -> Any:
    """Get worker data from a JSON file."""
    return load_json(file_path)


def from_xls_to_json(
    monthly_attendance_report_xsl_path: str = (
        MONTHLY_ATTENDANCE_REPORT_XLS_PATH
    ),
    worker_details_json_path: str = WORKER_DETAILS_JSON_PATH,
) -> List[Dict[str, Any]]:
    """Convert data from an Excel file to a JSON-compatible list of
    dictionaries.
        :param monthly_attendance_report_xsl_path: path to
        monthly working hours report in Excel format
        :param worker_details_json_path: path to worker details JSON file
    """
    workbook = openpyxl.load_workbook(monthly_attendance_report_xsl_path)
    sheet = workbook.active
    worker_data = get_worker_data(worker_details_json_path)
    workers = []

    for row in sheet.iter_rows(
        min_row=3, max_row=11, max_col=14, values_only=True
    ):
        worker = create_worker_dict(row, worker_data)
        if worker:
            workers.append(worker)

    return workers


def monthly_salary_workers_data(
    worker_hours_json_path: str = WORKER_HOURS_JSON_PATH,
    worker_details_json_path: str = WORKER_DETAILS_JSON_PATH,
) -> List[Dict[str, Any]]:
    worker_data = get_worker_data(worker_details_json_path)
    workers_hours = get_working_hours(worker_hours_json_path)
    workers = []

    for row in workers_hours:
        worker = create_worker_dict_from_json(row, worker_data)
        if worker:
            workers.append(worker)

    return workers


def create_worker_dict_from_json(
    worker_hours: Dict[str, Any], worker_data: Dict[str, Any]
) -> Dict[str, Any]:
    """Create a worker dictionary from a row of JSON data."""
    worker_id = worker_hours["id"]
    if worker_id not in worker_data:
        return {}

    worker = {
        "id": worker_id,
        "name": worker_data[worker_id]["name"],
        "worker_type": worker_data[worker_id]["worker_type"],
        "hours": worker_hours["hours"],
        "per_hour": worker_data[worker_id]["per_hour"],
        "reg_hours_sal": worker_hours["reg_hours_sal"],
        "hours_125": worker_hours["hours_125"],
        "per_hour_125": worker_data[worker_id]["per_hour_125"],
        "extra_hours_sal": worker_hours["extra_hours_sal"],
        "monthly_sal": worker_data[worker_id]["monthly_sal"],
        "trans_expanses": worker_data[worker_id]["trans_expanses"],
        "total_hours": worker_hours["total_hours"],
        "work_days": worker_hours["work_days"],
        "holidays": worker_hours["holidays"],
        "holiday_present": worker_hours["holiday_present"],
        "sick_days": worker_hours["sick_days"],
        "vac_days": worker_hours["vac_days"],
        "absense_hours": (
            worker_hours["absense_hours"]
            if worker_hours["worker_type"] == "monthly"
            else 0
        ),
        "total_sal": worker_hours["total_sal"],
    }

    calculate_salaries(worker)
    return worker


def create_worker_dict(
    row: tuple, worker_data: Dict[str, Any]
) -> Dict[str, Any]:
    """Create a worker dictionary from a row of Excel data."""
    worker_id = str(row[2])
    if worker_id not in worker_data:
        return {}

    worker = {
        "id": worker_id,
        "name": worker_data[worker_id]["name"],
        "worker_type": worker_data[worker_id]["worker_type"],
        "daily_hours": worker_data[worker_id]["daily_hours"],
        "hours": row[6],
        "per_hour": worker_data[worker_id]["per_hour"],
        "reg_hours_sal": 0,
        "hours_125": row[7],
        "per_hour_125": worker_data[worker_id]["per_hour_125"],
        "extra_hours_sal": 0,
        "monthly_sal": worker_data[worker_id]["monthly_sal"],
        "trans_expanses": worker_data[worker_id]["trans_expanses"],
        "total_hours": row[6],
        "work_days": row[3],
        "holidays": 0,
        "holiday_present": 0,
        "sick_days": row[12],
        "vac_days": row[13],
        "absense_hours": row[8],
        "total_sal": 0,
    }

    calculate_salaries(worker)
    return worker


def calculate_salaries(worker: Dict[str, Any]) -> None:
    """Calculate salaries for a worker."""
    if worker["worker_type"] == "hourly":
        worker["reg_hours_sal"] = (
            time_string_to_decimals(worker["hours"]) * worker["per_hour"]
        )
        worker["extra_hours_sal"] = (
            time_string_to_decimals(worker["hours_125"])
            * worker["per_hour_125"]
        )
    elif worker["worker_type"] == "daily":
        worker["hours"] = worker["work_days"] * worker["daily_hours"]
        worker["total_hours"] = worker["hours"]
        worker["reg_hours_sal"] = worker["hours"] * worker["per_hour"]
    else:
        worker["reg_hours_sal"] = worker["monthly_sal"]

    if worker["reg_hours_sal"] == 0:
        worker["trans_expanses"] = 0

    worker["total_sal"] = (
        worker["reg_hours_sal"]
        + worker["extra_hours_sal"]
        + worker["trans_expanses"]
    )


def time_string_to_decimals(time_string: str) -> float:
    """Convert a time string in HH:MM:SS format to decimal hours."""
    try:
        fields = time_string.split(":")
        hours = float(fields[0]) if len(fields) > 0 else 0.0
        minutes = float(fields[1]) if len(fields) > 1 else 0.0
        seconds = float(fields[2]) if len(fields) > 2 else 0.0
        return hours + (minutes / 60.0) + (seconds / 3600.0)
    except (ValueError, AttributeError):
        return 0.0
