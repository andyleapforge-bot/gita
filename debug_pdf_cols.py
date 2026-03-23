"""
DEBUG: Print exact PDF columns to understand correct mapping
"""

import pdfplumber

pdf_path = r"D:\zita\Vita\SriMadBhagvadGita Reels _ Shorts _ Keywords & Links _ HINDI - Hindi Table.pdf"

with pdfplumber.open(pdf_path) as pdf:
    page = pdf.pages[0]
    tables = page.extract_tables()
    
    if tables:
        table = tables[0]
        row = table[2]
        
        print("PDF TABLE STRUCTURE - First Data Row")
        print("=" * 100)
        print(f"Total columns: {len(row)}\n")
        
        for col_idx, cell in enumerate(row):
            cell_str = str(cell)[:80] if cell else "EMPTY"
            cell_lines = cell_str.split('\n')
            if len(cell_lines) > 1:
                cell_str = cell_lines[0] + " | " + cell_lines[1] + "..."
            print(f"Col {col_idx:2d}: {cell_str}")
