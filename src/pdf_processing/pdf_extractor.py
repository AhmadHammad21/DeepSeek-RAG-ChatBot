import os
from PyPDF2 import PdfReader

class PDFExtractor:
    def __init__(self, pdf_dir):
        self.pdf_dir = pdf_dir

    def extract_text(self):
        documents = []
        for file in os.listdir(self.pdf_dir):
            if file.endswith(".pdf"):
                with open(os.path.join(self.pdf_dir, file), 'rb') as f:
                    pdf = PdfReader(f)
                    text = "".join([page.extract_text() for page in pdf.pages])
                    documents.append(text)
        return documents
