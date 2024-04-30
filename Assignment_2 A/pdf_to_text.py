import PyPDF2
import pypdfium2 as pdfium
import fitz
from tika import parser
import pytesseract
from PIL import Image


def pdf_to_text_pypdf2(pdf_file, output_file):
    text = "\n"

    with open(pdf_file, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        num_pages = len(pdf_reader.pages)
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
            text += "\n"

    with open(output_file, "w") as f:
        f.write(text)


def pdf_to_text_pypdfium2(pdf_file, output_file):
    text = "\n"

    pdf = pdfium.PdfDocument(pdf_file)
    num_pages = len(pdf)
    for page_num in range(num_pages):
        page = pdf[page_num]
        text += page.get_textpage().get_text_bounded()
        text += "\n"
    with open(output_file, "w") as f:
        f.write(text)


def pdf_to_text_pymupdf(pdf_file, output_file):
    text = "\n"

    with fitz.open(pdf_file) as pdf:
        for page_num in range(len(pdf)):
            page = pdf.load_page(page_num)
            text += page.get_text()
            text += "\n"
    with open(output_file, "w") as f:
        f.write(text)


def pdf_to_text_tika(pdf_file, output_file):
    parsed_pdf = parser.from_file(pdf_file)
    text = parsed_pdf["content"]
    with open(output_file, "w") as f:
        f.write(text)


def pdf_to_text_pytesseract(pdf_file, output_file):
    text = "\n"
    pdf_document = fitz.open(pdf_file)

    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)
        page_image = page.get_pixmap()
        image = Image.frombytes(
            "RGB", (page_image.width, page_image.height), page_image.samples
        )
        text += pytesseract.image_to_string(image) + "\n"

    with open(output_file, "w") as f:
        f.write(text)

pdf_to_text_pypdf2("pdfs/report.pdf", "out.txt")