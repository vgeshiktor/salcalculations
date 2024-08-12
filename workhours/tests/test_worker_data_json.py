import json
from typing import Any, List

import pytest


def validate_worker_data(worker_data: Any) -> List[str]:
    errors = []

    for worker_id, worker in worker_data.items():
        if not worker["name"]:
            errors.append(f"Worker {worker_id} has an empty name")

        if worker["worker_type"] not in ["monthly", "hourly"]:
            errors.append(
                f"Worker {worker_id} has invalid worker_type:"
                f" {worker['worker_type']}"
            )

        if worker["worker_type"] == "monthly" and worker["monthly_sal"] == 0:
            errors.append(
                f"Worker {worker_id} has monthly "
                f"worker_type but zero monthly_sal"
            )

        if worker["worker_type"] == "hourly" and worker["per_hour"] == 0:
            errors.append(
                f"Worker {worker_id} has hourly "
                f"worker_type but zero per_hour"
            )

        if worker["worker_type"] == "hourly" and worker["per_hour_125"] == 0:
            errors.append(
                f"Worker {worker_id} has hourly "
                f"worker_type but zero per_hour_125"
            )

        if worker["per_hour"] < 0:
            errors.append(
                f"Worker {worker_id} has negative "
                f"per_hour: {worker['per_hour']}"
            )

        if worker["per_hour_125"] < 0:
            errors.append(
                f"Worker {worker_id} has negative "
                f"per_hour_125: {worker['per_hour_125']}"
            )

        if worker["monthly_sal"] < 0:
            errors.append(
                f"Worker {worker_id} has negative "
                f"monthly_sal: {worker['monthly_sal']}"
            )

        if worker["trans_expanses"] < 0:
            errors.append(
                f"Worker {worker_id} has negative "
                f"trans_expanses: {worker['trans_expanses']}"
            )

        if worker["holidays"] < 0:
            errors.append(
                f"Worker {worker_id} has "
                f"negative holidays: {worker['holidays']}"
            )

        if worker["holiday_present"] < 0:
            errors.append(
                f"Worker {worker_id} has negative "
                f"holiday_present: {worker['holiday_present']}"
            )

    return errors


def load_worker_data(file_path: str) -> Any:
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


@pytest.fixture
def worker_data(pytestconfig) -> Any:
    return load_worker_data(f"{pytestconfig.rootpath}/config/id2worker.json")


def test_validate_worker_data(worker_data: Any) -> None:
    errors = validate_worker_data(worker_data)
    assert not errors, f"Validation errors found: {errors}"
