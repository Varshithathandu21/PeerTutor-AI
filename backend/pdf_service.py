"""
PDF Processing Service for PeerTutor AI
Handles complex PDF extraction including text, images, and tables
"""

import io
from typing import Dict, Any
import PyPDF2
import pdfplumber


class PDFService:
    @staticmethod
    def extract_text_pypdf2(pdf_bytes: bytes) -> str:
        """Extract text using PyPDF2 - simpler method"""
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            print(f"PyPDF2 extraction error: {e}")
            return ""
    
    @staticmethod
    def extract_text_pdfplumber(pdf_bytes: bytes) -> Dict[str, Any]:
        """
        Extract text using pdfplumber - handles complex PDFs better
        Extracts text, tables, and layout information
        """
        try:
            text_content = ""
            tables_content = []
            
            with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    # Extract text
                    page_text = page.extract_text()
                    if page_text:
                        text_content += f"\n--- Page {page_num} ---\n{page_text}\n"
                    
                    # Extract tables
                    tables = page.extract_tables()
                    if tables:
                        for table_idx, table in enumerate(tables, 1):
                            table_text = f"\n[Table {table_idx} on Page {page_num}]\n"
                            for row in table:
                                table_text += " | ".join([str(cell) if cell else "" for cell in row]) + "\n"
                            tables_content.append(table_text)
                            text_content += table_text
            
            return {
                "text": text_content,
                "tables": tables_content,
                "page_count": len(pdf.pages) if 'pdf' in locals() else 0
            }
        except Exception as e:
            print(f"pdfplumber extraction error: {e}")
            return {"text": "", "tables": [], "page_count": 0}
    
    @staticmethod
    def process_pdf(pdf_bytes: bytes) -> Dict[str, Any]:
        """
        Main method to process PDF - tries pdfplumber first, falls back to PyPDF2
        """
        result = PDFService.extract_text_pdfplumber(pdf_bytes)
        
        # If pdfplumber fails, try PyPDF2
        if not result["text"].strip():
            text = PDFService.extract_text_pypdf2(pdf_bytes)
            result = {
                "text": text,
                "tables": [],
                "page_count": 0
            }
        
        return result
