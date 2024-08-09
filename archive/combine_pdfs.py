import os
from pathlib import Path

import PyPDF2

# specify the directory containing the PDF files to be combined
pdf_dir = r'C:\Users\innas\OneDrive\Рабочий стол\workers\Victoria Brosilovski'

# get a list of the PDF files in the directory
# pdf_files = [filename for filename in os.listdir(pdf_dir) if filename.endswith('.pdf')]
pdf_files = [Path(rf'{pdf_dir}\{filename}') for filename in ('viktoria-brosilovski-161-2023-1.pdf', 'viktoria-brosilovski-161-2023-2.pdf')]

# create a new PDF file to hold the merged PDFs
output_pdf = PyPDF2.PdfMerger()

# add each PDF file to the output PDF
for filename in pdf_files:
    filepath = os.path.join(pdf_dir, filename)
    pdf_file = open(filepath, 'rb')
    output_pdf.append(pdf_file)

# write the output PDF to a file
output_filepath = os.path.join(pdf_dir, 'viktoria-brosilovski-161-2023-signed.pdf')
output_pdf.write(output_filepath)

# close all the open PDF files
output_pdf.close()
# for pdf_file in pdf_files:
#     pdf_file.close()
