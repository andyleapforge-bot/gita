"""
Deep dive into Chapter 18 extraction - check if verses 624-658 exist in PDF but are being missed.
"""
import pdfplumber

pdf_path = r"D:\zita\Vita\SriMadBhagvadGita Reels _ Shorts _ Keywords & Links _ HINDI - Hindi Table.pdf"

print("Checking all pages for any reference to verses 624-658 in Chapter 18...\n")

with pdfplumber.open(pdf_path) as pdf:
    for page_num, page in enumerate(pdf.pages):
        # Get raw text
        text = page.extract_text()
        
        # Check if page contains any of the missing verse numbers
        found_missing = False
        for v in range(624, 659):
            if str(v) in text:
                found_missing = True
                break
        
        if found_missing:
            print(f"✅ Page {page_num+1} contains verses in range 624-658")
            # Show detail
            tables = page.extract_tables()
            if tables:
                for t_idx, table in enumerate(tables):
                    if len(table) >= 3:
                        row = table[2]
                        verses_text = str(row[1]) if len(row) > 1 else ""
                        if any(str(v) in verses_text for v in range(624, 659)):
                            print(f"   Table {t_idx}: {verses_text[:100]}...")
        else:
            # Check if page has any Chapter 18
            has_ch18 = False
            for v in range(1, 79):
                if str(v) in text:
                    has_ch18 = True
                    break
            if has_ch18:
                print(f"Page {page_num+1}: Has Chapter 18 data")

print("\n" + "="*60)
print("CHECKING LAST 3 PAGES IN DETAIL:")
print("="*60)

for page_num in [12, 13, 14]:  # Pages 13, 14, 15 (indices 12, 13, 14)
    page = pdf.pages[page_num]
    tables = page.extract_tables()
    
    print(f"\nPage {page_num+1}:")
    if tables:
        for t_idx, table in enumerate(tables):
            print(f"  Table {t_idx}: {len(table)} rows × {len(table[0]) if table else 0} cols")
            if len(table) >= 3:
                row = table[2]
                # Extract verse numbers
                verses_str = str(row[1]) if len(row) > 1 else ""
                verses = [l.strip() for l in verses_str.split('\n') if l.strip() and l.strip().isdigit()]
                if verses:
                    print(f"    Verses: {verses[0]} to {verses[-1]} (count: {len(verses)})")
