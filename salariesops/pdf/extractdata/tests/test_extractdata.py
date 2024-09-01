import pytest
from PyPDF2 import PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from salariesops.pdf.extractdata.handler import extract_text_from_pdf


@pytest.fixture
def file_name(tmp_path) -> str:
    return str(tmp_path / "output.pdf")


@pytest.fixture
def text():
    return "Expected text from the PDF"


@pytest.fixture
def create_pdf(file_name, text):
    # Set up the PDF canvas with letter size
    pdf = canvas.Canvas(file_name, pagesize=letter)

    # Set the font and size
    pdf.setFont("Helvetica", 12)

    # Draw the text on the PDF at position x=100, y=750
    pdf.drawString(100, 750, text)

    # Save the PDF
    pdf.save()


def test_extracts_text_correctly(tmp_path, text, file_name, create_pdf):
    # Create a PDF with some text content
    text = extract_text_from_pdf(str(file_name)).strip()
    assert text == "Expected text from the PDF"


def test_handles_empty_pdf(tmp_path):
    pdf_path = tmp_path / "empty.pdf"
    writer = PdfWriter()
    writer.add_blank_page(width=72, height=72)
    with open(pdf_path, "wb") as f:
        writer.write(f)
    text = extract_text_from_pdf(str(pdf_path))
    assert text == ""


def test_raises_error_for_non_existent_pdf():
    with pytest.raises(FileNotFoundError):
        extract_text_from_pdf("non_existent.pdf")
