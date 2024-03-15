#!/usr/bin/env python

from PyPDF2 import PdfReader, PdfWriter
import io

def remove_images(input_pdf_path, output_pdf_path):
    # Open the PDF file
    with open(input_pdf_path, 'rb') as input_file:
        pdf_reader = PdfReader (input_file)
        pdf_writer = PdfWriter()

        # Iterate through each page
        for page_number in range (len (pdf_reader.pages)):
            page = pdf_reader.pages [page_number]
            # Remove images by creating a new page without images
            page_without_images = PdfReader(io.BytesIO(b'')).pages [0]
            #page_without_images = PdfReader(io.BytesIO(b'')).getPage(0)
            page_without_images.merge_page(page)
            pdf_writer.addPage(page_without_images)

        # Write the modified PDF to a new file
        with open(output_pdf_path, 'wb') as output_file:
            pdf_writer.write(output_file)

# Example usage
input_pdf_path = "input.pdf"
output_pdf_path = "output.pdf"
remove_images(input_pdf_path, output_pdf_path)

