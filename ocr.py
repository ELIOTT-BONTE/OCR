import easyocr
import fitz  # PyMuPDF

def extract_images_from_pdf(pdf_path):
    try:
        pdf_document = fitz.open(pdf_path)
        images = []
        
        for page_number in range(len(pdf_document)):
            page = pdf_document[page_number]
            pix = page.get_pixmap()
            images.append(pix.tobytes("png"))  # Convert to PNG bytes
        
        return images
    except Exception as e:
        raise RuntimeError(f"Failed to extract images from PDF: {e}")

def perform_ocr(file_path):

    try:
        # Initialize the EasyOCR reader
        reader = easyocr.Reader(['en'])  # Specify the language(s) you want to support
        
        if file_path.lower().endswith(".pdf"):
            # Handle PDF files
            images = extract_images_from_pdf(file_path)
            results = []
            for image_bytes in images:
                # Perform OCR on each extracted image
                text = reader.readtext(image_bytes, detail=0)
                results.append("\n".join(text))
            return "\n\n".join(results)
        else:
            # Handle image files
            results = reader.readtext(file_path, detail=0)  # detail=0 returns only the text
            return "\n".join(results)
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    file_path = "input/sample.pdf"  # Input goes here
    extracted_text = perform_ocr(file_path)
    print("Extracted Text:")
    print(extracted_text)