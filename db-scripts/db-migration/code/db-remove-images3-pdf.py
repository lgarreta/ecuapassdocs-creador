#!/usr/bin/env python3

import fitz  # PyMuPDF

def remove_images(pdf_path, output_path):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    
    # Iterate through each page
    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)
        # Get the list of images on the page
        images_list = page.get_images(full=True)
        # Remove each image from the page
        for img_index in range(len(images_list)):
            page.remove_image(img_index)
    
    # Save the modified PDF to a new file
    pdf_document.save(output_path)
    pdf_document.close()

# Example usage
input_pdf_path = "input.pdf"
output_pdf_path = "output.pdf"
remove_images(input_pdf_path, output_pdf_path)

