import os
import re
from PyPDF2 import PdfReader
from docx import Document
import logging

logger = logging.getLogger(__name__)

def extract_text_from_file(file_path):
    """Main entry point for text extraction"""
    try:
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext == '.pdf':
            return extract_text_pdf(file_path)
        elif ext == '.docx':
            return extract_text_docx(file_path)
        elif ext == '.txt':
            return extract_text_txt(file_path)
        else:
            raise ValueError(f"Unsupported file format: {ext}")
    
    except Exception as e:
        logger.error(f"Error extracting text from {file_path}: {str(e)}")
        raise

def extract_text_pdf(file_path):
    """Extract text from PDF files"""
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return normalize_text(text)
    except Exception as e:
        logger.error(f"PDF extraction error: {str(e)}")
        raise

def extract_text_docx(file_path):
    """Extract text from DOCX files"""
    try:
        doc = Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return normalize_text(text)
    except Exception as e:
        logger.error(f"DOCX extraction error: {str(e)}")
        raise

def extract_text_txt(file_path):
    """Extract text from TXT files"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        return normalize_text(text)
    except Exception as e:
        logger.error(f"TXT extraction error: {str(e)}")
        raise

def normalize_text(text):
    """Clean and normalize text"""
    if not text:
        return ""
    text = re.sub(r'\s+', ' ', text)
    return text.strip()
