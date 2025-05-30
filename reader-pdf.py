from pdfminer.high_level import extract_text

# Path to the PDF file
pdf_path = "extract.pdf"

# Extract text content from the PDF
text = extract_text(pdf_path)

# Check if the PDF contains readable text or is likely an image-based scan
if text.strip():
    print("✅ The PDF contains selectable text (not an image).")
else:
    print("⚠️ The PDF appears to be image-based (no extractable text).")
