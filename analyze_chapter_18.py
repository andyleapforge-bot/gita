"""
Analyze the Hindi PDF to find why Chapter 18 is incomplete.
"""
import pdfplumber

pdf_path = r"D:\zita\Vita\SriMadBhagvadGita Reels _ Shorts _ Keywords & Links _ HINDI - Hindi Table.pdf"

with pdfplumber.open(pdf_path) as pdf:
    print(f"Total PDF pages: {len(pdf.pages)}\n")
    
    total_entries_by_chapter = {}
    
    for page_num, page in enumerate(pdf.pages):
        tables = page.extract_tables()
        
        if not tables:
            print(f"Page {page_num+1}: No tables found")
            continue
        
        for table in tables:
            if len(table) < 3:
                continue
            
            # Get chapter column
            row = table[2]
            if len(row) < 3:
                continue
            
            chapters = str(row[2]).split('\n')
            verses = str(row[1]).split('\n')
            
            # Count unique chapters on this page
            chapters_on_page = {}
            for ch_text, v_text in zip(chapters, verses):
                try:
                    ch = int(ch_text.strip()) if ch_text.strip() else 0
                    v = int(v_text.strip()) if v_text.strip() else 0
                    if ch > 0 and v > 0:
                        if ch not in chapters_on_page:
                            chapters_on_page[ch] = []
                        chapters_on_page[ch].append(v)
                except:
                    pass
            
            if chapters_on_page:
                print(f"Page {page_num+1}:")
                for ch in sorted(chapters_on_page.keys()):
                    verses_list = sorted(chapters_on_page[ch])
                    if ch not in total_entries_by_chapter:
                        total_entries_by_chapter[ch] = 0
                    total_entries_by_chapter[ch] += len(verses_list)
                    print(f"  Chapter {ch}: verses {min(verses_list)}-{max(verses_list)} ({len(verses_list)} total on this table)")

print(f"\n{'='*60}")
print("TOTAL EXTRACTED VERSES BY CHAPTER:")
print(f"{'='*60}")
for ch in sorted(total_entries_by_chapter.keys()):
    print(f"Chapter {ch}: {total_entries_by_chapter[ch]} verses")

print(f"\nTotal entries extracted: {sum(total_entries_by_chapter.values())}")
