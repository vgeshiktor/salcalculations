from pdf2image import convert_from_path

# PIL.Image.MAX_IMAGE_PIXELS = 933120000

pages = convert_from_path(
    rf"C:\Users\innas\OneDrive\Рабочий стол\bait ham\receipts\sxirut\shirut-02-2024 (2).pdf",
    200,
    poppler_path=r"C:\poppler-23.01.0\Library\bin",
)
page_num = 1
for page in pages:
    file = rf"C:\Users\innas\OneDrive\Рабочий стол\bait ham\receipts\sxirut\shirut-02-2024 (2).jpg"
    print(rf"creating file: {file}")
    page.save(file, "JPEG")
    page_num += 1
