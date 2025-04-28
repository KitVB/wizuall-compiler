# preprocessor/pdf_extractor.py
import PyPDF2
import re
import numpy as np

class PDFExtractor:
    def __init__(self, file_path):
        self.file_path = file_path
        
    def extract_text(self):
        """Extract raw text from PDF file"""
        with open(self.file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
        return text
    
    def extract_numeric_data(self):
        """Parse text to extract numeric data"""
        text = self.extract_text()
        # Find all numbers in text
        numbers = re.findall(r"[-+]?\d*\.\d+|\d+", text)
        return [float(num) for num in numbers]
    
    def extract_labeled_data(self):
        """Extract labeled numeric data (e.g., table-like structures)"""
        # More complex extraction logic here
        # Return dictionary or data structure with labels
        pass