import re

from PyPDF2 import PdfReader


def extract_text_from_pdf(pdf_path: str) -> str:
    pdf = PdfReader(pdf_path)
    text = ""
    for page in pdf.pages:
        text += page.extract_text()
    return text


def parse_personal_info(input_text):
    info = {}
    patterns = {
        "Employee Name": r"-(\W|$)(^\S*)לכבוד",
        "Address": r"סמינלנסקי 27, פתח תקווה 0",
        "Employee Number": r"מספר העובד: (\d+)",
        "Identity Number": r"מספר זהות: (\d+)",
        "Resident": r"תושב: (\S+)",
        "Main Job": r"משרה בי\"ל: (\S+)",
        "Job Unit": r"ס\.משרה: (\S+)",
        "Seniority": r"וותק: (\S+)",
        "Job Fraction": r"חלקיות המשרה: (\S+)",
        "Salary Basis": r"בסיס השכר: (\S+)",
        "Job Start Date": r"תחילת עבודה: (\S+)",
        "Department": r"מחלקה: (\S+)",
        "Marital Status": r"מצב משפחתי: (\S+)",
        "Rank": r"דרגה: (\S+)",
        "Rating": r"דרוג: (\S+)",
        "Bank Account Number": r"חשבון: (\d+)",
        "Bank Number": r"בנק: (\d+/\d+)",
    }
    for key, pattern in patterns.items():
        match = re.search(pattern, input_text)
        info[key] = match.group(1) if match else ""
    print(info)
    return info


if __name__ == "__main__":
    input_pdf = "./input/salary-example.pdf"  # Replace with your PDF file path
    input_pdf = "./output/page_1.pdf"  # Replace with your PDF file
    # path
    text = extract_text_from_pdf(input_pdf)
    # print(text)
    personal_info = parse_personal_info(text)
    print(personal_info)
