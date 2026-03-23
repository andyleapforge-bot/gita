import pdfplumber
import json

pdf_path = 'SriMadBhagvadGita Reels _ Shorts _ Keywords & Links _ HINDI - Hindi Table.pdf'

hindi_data = {}

try:
    with pdfplumber.open(pdf_path) as pdf:
        # Try to extract tables from all pages
        for page_num, page in enumerate(pdf.pages, 1):
            tables = page.extract_tables()
            if tables:
                for table in tables:
                    for row in table:
                        # Try to parse chapter and shlok numbers
                        if row and len(row) > 0:
                            print(f"Page {page_num}: {row[:3]}")  # Show first 3 columns
            
            # Also try text extraction
            text = page.extract_text()
            if text:
                print(f"\n=== Page {page_num} Text ===")
                print(text[:300])
                print()

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
