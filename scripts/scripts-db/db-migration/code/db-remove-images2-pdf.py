#!/usr/bin/env python
import fitz  # Install PyMuPDF using `pip install fitz`

def remove_images(pdf_path, output_path):
  """
  Removes images from a PDF by replacing them with empty objects.

  Args:
    pdf_path: Path to the input PDF file.
    output_path: Path to save the modified PDF file.
  """
  doc = fitz.open(pdf_path)
  for page in doc:
    blocks = page.get_text("blocks")
    for block in blocks:
      if block[1] == fitz.IMAGE:  # Check if block is an image
        block[4] = fitz.Rect(0, 0, 0, 0)  # Replace with empty rectangle
  doc.save(output_path)

if __name__ == "__main__":
  pdf_path = "input.pdf"
  output_path = "output.pdf"
  remove_images(pdf_path, output_path)
  print("Images removed and saved to", output_path)

