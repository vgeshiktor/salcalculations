from typing import Any, Dict, List

import openpyxl
from openpyxl.styles import Alignment, Border, Font, Side
from openpyxl.worksheet.worksheet import Worksheet

from workinghours import from_xls_to_json, monthly_salary_workers_data

# Constants
HEADER_FONT = Font(bold=True, size=14)
TEXT_FONT = Font(size=14)
ALIGN_CENTER = Alignment(horizontal="center")
ALIGN_LEFT = Alignment(horizontal="left")
ALIGN_RIGHT = Alignment(horizontal="right")
THICK_BORDER = Border(
    left=Side(style="thick"),
    right=Side(style="thick"),
    top=Side(style="thick"),
    bottom=Side(style="thick"),
)

# File path constants
MONTHLY_ATTENDANCE_REPORT_XLS_PATH = "input/08-2024.xlsx"
WORKER_HOURS_JSON_PATH = "input/workershours.json"
WORKER_DETAILS_JSON_PATH = "config/id2worker.json"
SALARY_DETAILS_OUTPUT_PATH = "output/salary_details.xlsx"


def load_workers_monthly_attendance_data(
    monthly_attendance_report_xsl_path: str, worker_details_json_path: str
) -> List[Dict[str, Any]]:
    """Load workers data from Excel and JSON files."""
    try:
        return from_xls_to_json(
            monthly_attendance_report_xsl_path, worker_details_json_path
        )
    except Exception as e:
        print(f"Error loading workers data: {e}")
        return []


def create_workbook() -> openpyxl.Workbook:
    """Create a new workbook and set initial properties."""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.sheet_view.rightToLeft = True
    ws.title = "Salary Details"
    return wb


def write_worker_data(
    ws: Worksheet,
    worker: Dict[str, Any],
    start_row: int,
) -> int:
    """Write worker data to the worksheet starting from the given row."""

    def write_cell(
        row,
        col,
        value,
        font=TEXT_FONT,
        alignment=ALIGN_LEFT,
        border=THICK_BORDER,
        number_format=None,
    ):
        cell = ws.cell(row=row, column=col, value=value)
        cell.font = font
        cell.alignment = alignment
        cell.border = border
        if number_format:
            cell.number_format = number_format

    write_cell(start_row, 1, worker["name"], HEADER_FONT, ALIGN_RIGHT)

    # Writing title in the second row of the table
    write_cell(start_row + 1, 1, None)
    write_cell(start_row + 1, 2, "שעות", HEADER_FONT)
    write_cell(start_row + 1, 3, "לשעה ₪", HEADER_FONT)
    write_cell(start_row + 1, 4, 'סה"כ ₪', HEADER_FONT)

    # Writing regular hours row in the 3rd row of the table
    write_cell(start_row + 2, 1, "ש.רגילות", HEADER_FONT)
    write_cell(start_row + 2, 2, worker["hours"])
    write_cell(start_row + 2, 3, worker["per_hour"])
    write_cell(start_row + 2, 4, worker["reg_hours_sal"], number_format="#")

    # Empty row (start_row + 3)

    # Writing extra hours row in the 4th row of the table
    write_cell(start_row + 4, 1, "ש.נ. 125%", HEADER_FONT)
    write_cell(start_row + 4, 2, worker["hours_125"])
    write_cell(start_row + 4, 3, worker["per_hour_125"])
    write_cell(start_row + 4, 4, worker["extra_hours_sal"], number_format="#")

    # Empty row (start_row + 5)

    # Writing transportation expenses row in the 6th row of the table
    write_cell(start_row + 6, 1, "נסיעות", HEADER_FONT)
    write_cell(start_row + 6, 4, worker["trans_expanses"])

    # Writing total salary row in the 7th row of the table
    write_cell(start_row + 7, 1, 'סה"כ', HEADER_FONT)
    write_cell(start_row + 7, 2, worker["total_hours"])
    write_cell(start_row + 7, 4, worker["total_sal"], number_format="#")

    # Empty row (start_row + 8)

    # Writing work days row in the 9th row of the table
    write_cell(start_row + 9, 1, "ימי עבודה", HEADER_FONT)
    write_cell(start_row + 9, 2, worker["work_days"])

    # Writing holiday row in the 10th row of the table
    write_cell(start_row + 10, 1, "חג", HEADER_FONT)
    write_cell(start_row + 10, 2, worker["holidays"])

    # Writing gift row in the 11th row of the table
    write_cell(start_row + 11, 1, "מתנה", HEADER_FONT)
    write_cell(start_row + 11, 2, worker["holiday_present"])

    # Writing sick days row in the 12th row of the table
    write_cell(start_row + 12, 1, "ימי מחלה", HEADER_FONT)
    write_cell(start_row + 12, 2, worker["sick_days"])

    # Writing vacation days row in the 13th row of the table
    write_cell(start_row + 13, 1, "ימי חופש", HEADER_FONT)
    write_cell(start_row + 13, 2, worker["vac_days"])

    # Write absense hours row in the 14th row of the table
    write_cell(start_row + 14, 1, "שעות להוריד", HEADER_FONT)
    write_cell(start_row + 14, 2, worker["absense_hours"])

    # Adding some space between tables
    return start_row + 18


def set_column_widths(ws: Worksheet) -> None:
    """Set column widths for better readability."""
    ws.column_dimensions["A"].width = 20
    ws.column_dimensions["B"].width = 20
    ws.column_dimensions["C"].width = 20
    ws.column_dimensions["D"].width = 20


def save_workbook(wb: openpyxl.Workbook, file_path: str) -> None:
    """Save the workbook to the specified file path."""
    try:
        wb.save(file_path)
    except Exception as e:
        print(f"Error saving workbook: {e}")


def main() -> None:
    # Load workers data from Excel and JSON files
    workers = load_workers_monthly_attendance_data(
        MONTHLY_ATTENDANCE_REPORT_XLS_PATH, WORKER_DETAILS_JSON_PATH
    )

    # append monthly salary workers that do not appear in the attendance report
    workers.extend(
        monthly_salary_workers_data(
            WORKER_HOURS_JSON_PATH, WORKER_DETAILS_JSON_PATH
        )
    )

    # create the workbook
    wb = create_workbook()
    ws = wb.active

    start_row = 1
    for worker in workers:
        start_row = write_worker_data(ws, worker, start_row)

    set_column_widths(ws)
    save_workbook(wb, SALARY_DETAILS_OUTPUT_PATH)


if __name__ == "__main__":
    main()
