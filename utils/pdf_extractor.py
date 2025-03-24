import pdfplumber

class PDFExtractor:
    def extract_text(self, pdf_path):
        """
        Extract text from a PDF file.
        :param pdf_path: Path to the PDF file
        :return: Extracted text or None if no text is found
        """
        try:
            with pdfplumber.open(pdf_path) as pdf:
                text = "\n".join([page.extract_text() or "" for page in pdf.pages])
                
            return text if text.strip() else None  # Return None if text is empty

        except Exception as e:
            print(f"Error extracting text from PDF: {e}")  # Log the error
            raise Exception(f"Error extracting text from PDF: {str(e)}")
