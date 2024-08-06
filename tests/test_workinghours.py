import pytest
from workinghours import load_json, get_working_hours, get_worker_data, from_xls_to_json, create_worker_dict, \
    calculate_salaries, time_string_to_decimals


@pytest.fixture
def valid_json_file_path():
    return '../id2worker.json'


@pytest.fixture
def invalid_json_file_path():
    return 'invalid_file.json'


@pytest.fixture
def valid_working_hours_file_path():
    return '../workershours.json'


@pytest.fixture
def valid_worker_data():
    return {"worker_id": {"worker_type": "hourly", "per_hour": 20}}


@pytest.fixture
def valid_worker_data_dict():
    return {
        "1": {"worker_type": "hourly", "per_hour": 20, "per_hour_125": 25, "monthly_sal": 3000, "trans_expanses": 100}
    }


@pytest.fixture
def working_hours_report_path():
    return '../report_example.xlsx'


@pytest.fixture
def valid_row():
    return None, None, "1", None, None, "40:00:00", "30:00:00", "10:00:00", None, None, None, None, "2", "1"


def test_load_json_valid_file(valid_json_file_path):
    data = load_json(valid_json_file_path)
    assert data != {}


def test_load_json_invalid_file(invalid_json_file_path):
    data = load_json(invalid_json_file_path)
    assert data == {}


def test_get_working_hours_valid_file(valid_working_hours_file_path):
    data = get_working_hours(valid_working_hours_file_path)
    assert data != {}


def test_get_worker_data_valid_file(valid_json_file_path, valid_worker_data):
    data = get_worker_data(valid_json_file_path)
    assert data != {}


def test_from_xls_to_json_valid_file(working_hours_report_path, valid_json_file_path):
    data = from_xls_to_json(working_hours_report_path, valid_json_file_path)
    assert len(data) > 0


def test_create_worker_dict_valid_data(valid_worker_data_dict, valid_row):
    worker = create_worker_dict(valid_row, valid_worker_data_dict)
    assert worker["id"] == "1"
    assert worker["worker_type"] == "hourly"


def test_calculate_salaries_hourly_worker():
    worker = {"worker_type": "hourly", "hours": "30:00:00", "per_hour": 20, "hours_125": "10:00:00", "per_hour_125": 25,
              "monthly_sal": 0, "trans_expanses": 100}
    calculate_salaries(worker)
    assert worker["reg_hours_sal"] == 600
    assert worker["extra_hours_sal"] == 250
    assert worker["total_sal"] == 950


def test_time_string_to_decimals_valid_time():
    result = time_string_to_decimals("01:30:00")
    assert result == 1.5


def test_time_string_to_decimals_invalid_time():
    result = time_string_to_decimals("invalid")
    assert result == 0.0
