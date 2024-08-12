# import the library
import PyPDF2

# open the PDF file
pdf_file = open(
    r"C:\Users\innas\OneDrive\Рабочий стол\bait ham\kvutzot\2023-2024.pdf",
    "rb",
)

# create a PDF Reader object
pdf_reader = PyPDF2.PdfReader(pdf_file)

page_num = 1

# loop through the pages
for page_num in range(len(pdf_reader.pages)):
    # create a PDF Writer object for each page
    pdf_writer = PyPDF2.PdfWriter()

    # add the page to the writer object
    page = pdf_reader.pages[page_num]
    pdf_writer.add_page(page)

    # create a new file
    page_file_name = rf"C:\Users\innas\OneDrive\Рабочий стол\bait ham\kvutzot\kvutza-{page_num}.pdf"
    new_pdf_file = open(page_file_name, "wb")

    # write the page to a new file
    pdf_writer.write(new_pdf_file)

    # close new pdf file
    new_pdf_file.close()

    page_num += 1

# close the original PDF file
pdf_file.close()
