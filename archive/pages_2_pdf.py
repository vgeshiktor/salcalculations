import subprocess

# Replace input_file.pages with the name and path of your .pages file
input_file = r'C:\Users\innas\Downloads\heskem1.pages'

# Replace output_file.pdf with the name and path of the PDF file you want to create
output_file = r'heskem1.pdf'

# Call the libreoffice command to convert the .pages file to PDF
subprocess.call(['libreoffice', '--headless', '--convert-to', 'pdf', input_file, '--outdir', './'])

# Rename the output file to the desired name
print('trying to process file: ')
subprocess.call(['mv', './'+input_file.replace('.pages', '.pdf'), output_file])
