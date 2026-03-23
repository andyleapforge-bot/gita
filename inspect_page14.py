"""
Detailed inspection of page 14 to find missing verses.
"""
import pdfplumber

pdf_path = r"D:\zita\Vita\SriMadBhagvadGita Reels _ Shorts _ Keywords & Links _ HINDI - Hindi Table.pdf"

with pdfplumber.open(pdf_path) as pdf:
    page = pdf.pages[13]  # Page 14 (0-indexed)
    
    print("PAGE 14 DETAILED INSPECTION:")
    print("="*60)
    
    # Get raw text
    text = page.extract_text()
    
    # Search for verse numbers 624-658
    print("\nVerse numbers found on page 14:")
    found_verses = set()
    for v in range(1, 750):
        if str(v) in text:
            found_verses.add(v)
    
    # Show the range
    sorted_verses = sorted(found_verses)
    print(f"Verse numbers present: {sorted_verses}")
    
    # Extract tables
    tables = page.extract_tables()
    print(f"\nNumber of tables: {len(tables) if tables else 0}")
    
    if tables:
        for t_idx, table in enumerate(tables):
            print(f"\n--- Table {t_idx} ---")
            print(f"Rows: {len(table)}, Columns: {len(table[0]) if table else 0}")
            
            for row_idx, row in enumerate(table):
                if row_idx == 0:
                    print(f"Row {row_idx} (header): (empty row)")
                    continue
                
                # Show first few columns
                print(f"Row {row_idx}:")
                for col_idx in range(min(4, len(row))):
                    cell_val = str(row[col_idx])[:80] if row[col_idx] else "(empty)"
                    if '\n' in cell_val:
                        lines = cell_val.split('\n')
                        print(f"  Col {col_idx}: {lines[0]}... ({len(lines)} lines)")
                    else:
                        print(f"  Col {col_idx}: {cell_val}")
