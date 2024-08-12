from typing import Any, Dict, Tuple

import pytest

from workhours.workinghours import (calculate_salaries, create_worker_dict,
                                    from_xls_to_json, get_worker_data,
                                    get_working_hours, load_json,
                                    time_string_to_decimals)


@pytest.fixture
def valid_json_file_path(pytestconfig) -> str:
    return f"{pytestconfig.rootpath}/config/id2worker.json"


@pytest.fixture
def invalid_json_file_path() -> str:
    return "invalid_file.json"


@pytest.fixture
def valid_working_hours_file_path(pytestconfig) -> str:
    return f"{pytestconfig.rootpath}/input/workershours.json"


@pytest.fixture
def valid_worker_data() -> Dict[str, Any]:
    return {"worker_id": {"worker_type": "hourly", "per_hour": 20}}


@pytest.fixture
def valid_worker_data_dict() -> Dict[str, Any]:
    return {
        "1": {
            "worker_type": "hourly",
            "per_hour": 20,
            "per_hour_125": 25,
            "monthly_sal": 3000,
            "trans_expanses": 100,
        }
    }


@pytest.fixture
def working_hours_report_path(pytestconfig) -> str:
    return f"{pytestconfig.rootpath}/input/report_example.xlsx"


@pytest.fixture
def valid_row() -> Tuple:
    return (
        None,
        None,
        "1",
        None,
        None,
        "40:00:00",
        "30:00:00",
        "10:00:00",
        None,
        None,
        None,
        None,
        "2",
        "1",
    )


def test_load_json_valid_file(valid_json_file_path: str) -> None:
    data = load_json(valid_json_file_path)
    assert data != {}


def test_load_json_invalid_file(invalid_json_file_path: str) -> None:
    data = load_json(invalid_json_file_path)
    assert data == {}


def test_get_working_hours_valid_file(
    valid_working_hours_file_path: str,
) -> None:
    data = get_working_hours(valid_working_hours_file_path)
    assert data != {}


def test_get_worker_data_valid_file(
    valid_json_file_path: str, valid_worker_data: Dict[str, Any]
) -> None:
    data = get_worker_data(valid_json_file_path)
    assert data != {}


def test_from_xls_to_json_valid_file(
    working_hours_report_path: str, valid_json_file_path: str
) -> None:
    data = from_xls_to_json(working_hours_report_path, valid_json_file_path)
    assert len(data) > 0


def test_create_worker_dict_valid_data(
    valid_worker_data_dict: Dict[str, Any], valid_row: Tuple
) -> None:
    worker = create_worker_dict(valid_row, valid_worker_data_dict)
    assert worker["id"] == "1"
    assert worker["worker_type"] == "hourly"


def test_calculate_salaries_hourly_worker() -> None:
    worker = {
        "worker_type": "hourly",
        "hours": "30:00:00",
        "per_hour": 20,
        "hours_125": "10:00:00",
        "per_hour_125": 25,
        "monthly_sal": 0,
        "trans_expanses": 100,
    }
    calculate_salaries(worker)
    assert worker["reg_hours_sal"] == 600
    assert worker["extra_hours_sal"] == 250
    assert worker["total_sal"] == 950


def test_time_string_to_decimals_valid_time() -> None:
    result = time_string_to_decimals("01:30:00")
    assert result == 1.5


def test_time_string_to_decimals_invalid_time() -> None:
    result = time_string_to_decimals("invalid")
    assert result == 0.0
