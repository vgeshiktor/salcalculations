import os

import pytest
from PyPDF2 import PdfReader

from salariesops.pdf.split2pages.handler import split_pdf


def test_splits_pdf_into_individual_pages(tmp_path):
    input_pdf_path = "../input/salary-example.pdf"  # Replace with a valid
    # test PDF path
    output_folder = tmp_path / "output"
    split_pdf(input_pdf_path, output_folder)
    assert len(os.listdir(output_folder)) == len(
        PdfReader(input_pdf_path).pages
    )


def test_creates_output_folder_if_not_exists(tmp_path):
    input_pdf_path = (
        "../input/salary-example.pdf"  # Replace with a valid test PDF path
    )
    output_folder = tmp_path / "new_output"
    split_pdf(input_pdf_path, output_folder)
    assert os.path.exists(output_folder)


def test_handles_non_existent_input_pdf(tmp_path):
    input_pdf_path = "../input/non_existent.pdf"
    output_folder = tmp_path / "output"
    with pytest.raises(FileNotFoundError):
        split_pdf(input_pdf_path, output_folder)


def test_handles_empty_pdf(tmp_path):
    input_pdf_path = "./input/empty.pdf"  # Replace with a valid empty PDF path
    output_folder = tmp_path / "output"
    split_pdf(input_pdf_path, output_folder)
    assert len(os.listdir(output_folder)) == 0
