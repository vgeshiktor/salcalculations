import PIL
from PIL import Image

PIL.Image.MAX_IMAGE_PIXELS = 933120000


def convert_to_pdf(image_path, output_path):
    with Image.open(image_path) as im:
        im.save(output_path, "PDF", resolution=100.0)


# Example usage
convert_to_pdf(
    rf"C:\Users\innas\OneDrive\Рабочий стол\bait ham\remont\sprinklers-zohar\sprinklers3-0080.jpg",
    rf"C:\Users\innas\OneDrive\Рабочий стол\bait ham\remont\sprinklers-zohar\sprinklers3-0080.pdf",
)
