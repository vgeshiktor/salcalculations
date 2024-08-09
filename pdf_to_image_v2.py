from PIL import Image
import os


def pdf_to_jpg(pdf_file, output_dir):
    # Open the PDF
    with Image.open(pdf_file) as img:
        # Get the number of pages in the PDF
        pages = img.n_frames
        # Loop through each page
        for i in range(pages):
            # Set the current page
            img.seek(i)
            # Save the current page as a JPG
            jpg_file = os.path.join(output_dir, f'page_{i}.jpg')
            img.save(jpg_file, 'JPEG')


if __name__ == '__main__':
    pdf_file = 'page-0.pdf'
    output_dir = '.'
    pdf_to_jpg(pdf_file, output_dir)
