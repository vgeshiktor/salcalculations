import PyPDF2

FILE_PATH = rf'C:\Users\innas\OneDrive\Рабочий стол\bait ham\kvutzot\kvutza-0.pdf'

with open(FILE_PATH, mode='rb') as f:

    reader = PyPDF2.PdfReader(f)

    page = reader.pages[0]

    print(page.extract_text())
    