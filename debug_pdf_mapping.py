"""
Debug script to show exact PDF column mapping.
"""
import pdfplumber

pdf_path = r"D:\zita\Vita\SriMadBhagvadGita Reels _ Shorts _ Keywords & Links _ HINDI - Hindi Table.pdf"

with pdfplumber.open(pdf_path) as pdf:
    page = pdf.pages[0]
    tables = page.extract_tables()
    
    if tables:
        t = tables[0]
        
        print("PDF TABLE STRUCTURE (Page 1)")
        print(f"Total rows: {len(t)}, Columns: {len(t[0])}\n")
        
        # Print header row (Row 0)
        print("=== Row 0 (Header) ===")
        for col_idx, cell in enumerate(t[0]):
            preview = str(cell)[:50] if cell else "(empty)"
            print(f"Col {col_idx:2d}: {preview}")
        
        # Print row 1 structure
        print("\n=== Row 1 ===")
        for col_idx, cell in enumerate(t[1]):
            preview = str(cell)[:50] if cell else "(empty)"
            print(f"Col {col_idx:2d}: {preview}")
        
        # Print row 2 (first data) - show first few items per column
        print("\n=== Row 2 (First data row) ===")
        row = t[2]
        for col_idx, cell in enumerate(row):
            if not cell:
                print(f"Col {col_idx:2d}: (empty)")
                continue
            
            lines = str(cell).split('\n')
            preview_lines = lines[:3]
            print(f"Col {col_idx:2d}: ({len(lines)} items)")
            for line in preview_lines:
                print(f"         - {line[:50]}")
            if len(lines) > 3:
                print(f"         - ... and {len(lines)-3} more")
