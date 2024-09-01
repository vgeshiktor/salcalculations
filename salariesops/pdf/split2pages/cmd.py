import argparse

from salariesops.pdf.split2pages.handler import split_pdf


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="splitpdf", description="Split a PDF into individual pages."
    )
    parser.add_argument("input_pdf", help="Path to the input PDF file.")
    parser.add_argument(
        "output_folder",
        help="Path to the output folder where individual pages will be saved.",
    )

    args = parser.parse_args()

    split_pdf(args.input_pdf, args.output_folder)
