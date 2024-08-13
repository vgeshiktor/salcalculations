import os

from PyPDF2 import PdfReader, PdfWriter


def split_pdf(input_pdf_path, output_folder):
    # Create a PDF reader object
    pdf_reader = PdfReader(input_pdf_path)

    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Loop through all the pages and save them individually
    for page_num in range(len(pdf_reader.pages)):
        pdf_writer = PdfWriter()
        pdf_writer.add_page(pdf_reader.pages[page_num])

        output_pdf_path = os.path.join(
            output_folder, f"page_{page_num + 1}.pdf"
        )
        with open(output_pdf_path, "wb") as output_pdf_file:
            pdf_writer.write(output_pdf_file)
            print(f"Saved: {output_pdf_path}")


if __name__ == "__main__":
    input_pdf = "./input/salary-example.pdf"  # Replace with your PDF file path
    output_dir = "output"  # Replace with your desired output folder
    split_pdf(input_pdf, output_dir)
