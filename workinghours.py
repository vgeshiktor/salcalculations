import json
import openpyxl
from typing import List, Dict, Any


def load_json(file_path: str) -> Dict[str, Any]:
    """Load JSON data from a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading JSON file {file_path}: {e}")
        return {}


def get_working_hours(file_path: str = 'workershours.json') -> Dict[str, Any]:
    """Get working hours from a JSON file."""
    return load_json(file_path)


def get_worker_data(file_path: str) -> Dict[str, Any]:
    """Get worker data from a JSON file."""
    return load_json(file_path)


def from_xls_to_json(monthly_attendance_report_xsl_path: str = 'report_example.xlsx',
                     worker_details_json_path: str = 'id2worker.json') -> List[Dict[str, Any]]:
    """Convert data from an Excel file to a JSON-compatible list of dictionaries.
    :param monthly_attendance_report_xsl_path: path to monthly working hours report in Excel format
    :param worker_details_json_path: path to worker details JSON file
    """
    workbook = openpyxl.load_workbook(monthly_attendance_report_xsl_path)
    sheet = workbook.active

    headers = [cell.value for cell in sheet[1]]
    worker_data = get_worker_data(worker_details_json_path)

    workers = []

    for row in sheet.iter_rows(min_row=3, max_row=11, max_col=14, values_only=True):
        worker = create_worker_dict(row, worker_data)
        if worker:
            workers.append(worker)

    return workers


def create_worker_dict(row: tuple, worker_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create a worker dictionary from a row of Excel data."""
    worker_id = str(row[2])
    if worker_id not in worker_data:
        return {}

    worker = {
        "id": worker_id,
        "name": worker_data[worker_id]['name'],
        "worker_type": worker_data[worker_id]['worker_type'],
        "hours": row[6],
        "per_hour": worker_data[worker_id]['per_hour'],
        "reg_hours_sal": 0,
        "hours_125": row[7],
        "per_hour_125": worker_data[worker_id]['per_hour_125'],
        "extra_hours_sal": 0,
        "monthly_sal": worker_data[worker_id]['monthly_sal'],
        "trans_expanses": worker_data[worker_id]['trans_expanses'],
        "total_hours": row[5],
        "work_days": row[3],
        "holidays": 0,
        "holiday_present": 0,
        "sick_days": row[12],
        "vac_days": row[13],
        "absense_hours": row[8],
        "total_sal": 0
    }

    calculate_salaries(worker)
    return worker


def calculate_salaries(worker: Dict[str, Any]) -> None:
    """Calculate salaries for a worker."""
    if worker['worker_type'] == 'hourly':
        worker['reg_hours_sal'] = time_string_to_decimals(worker['hours']) * worker['per_hour']
        worker['extra_hours_sal'] = time_string_to_decimals(worker['hours_125']) * worker['per_hour_125']
    else:
        worker['reg_hours_sal'] = worker['monthly_sal']

    worker['total_sal'] = worker['reg_hours_sal'] + worker['extra_hours_sal'] + worker['trans_expanses']


def time_string_to_decimals(time_string: str) -> float:
    try:
        """Convert a time string in HH:MM:SS format to decimal hours."""
        fields = time_string.split(":")
        hours = float(fields[0]) if len(fields) > 0 else 0.0
        minutes = float(fields[1]) if len(fields) > 1 else 0.0
        seconds = float(fields[2]) if len(fields) > 2 else 0.0
        return hours + (minutes / 60.0) + (seconds / 3600.0)
    except (ValueError, AttributeError):
        return 0.0
