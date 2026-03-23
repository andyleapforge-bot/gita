import pdfplumber
import json
import re
from pathlib import Path

# PDF file path
pdf_path = r"D:\zita\Vita\SriMadBhagvadGita Reels _ Shorts _ Keywords & Links _ HINDI - Hindi Table.pdf"

# Output JSON path
output_path = r"D:\zita\Vita\assets\json\shlok_data_hindi.json"

shloks = []

try:
    with pdfplumber.open(pdf_path) as pdf:
        print(f"Total pages: {len(pdf.pages)}\n")
        
        # First, let's examine the structure
        for page_num in range(min(2, len(pdf.pages))):
            page = pdf.pages[page_num]
            print(f"=== Page {page_num + 1} Analysis ===")
            
            # Try to extract tables
            tables = page.extract_tables()
            print(f"Tables found: {len(tables) if tables else 0}")
            
            if tables:
                for t_idx, table in enumerate(tables):
                    print(f"Table {t_idx + 1}: {len(table)} rows, {len(table[0]) if table else 0} columns")
                    # Print first 3 rows
                    for i, row in enumerate(table[:3]):
                        print(f"  Row {i}: {row[:3]}...")  # Print first 3 columns
            
            # Try text extraction
            text = page.extract_text()
            print(f"\nText length: {len(text) if text else 0} characters")
            print(f"First 500 chars:\n{text[:500] if text else 'No text'}\n")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
