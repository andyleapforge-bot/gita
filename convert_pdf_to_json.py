import pdfplumber
import json
from pathlib import Path

pdf_path = r"D:\zita\Vita\SriMadBhagvadGita Reels _ Shorts _ Keywords & Links _ HINDI - Hindi Table.pdf"
output_path = r"D:\zita\Vita\assets\json\shlok_data_hindi.json"

shloks = []

try:
    with pdfplumber.open(pdf_path) as pdf:
        print(f"Total pages: {len(pdf.pages)}\n")
        
        for page_num, page in enumerate(pdf.pages):
            print(f"Processing page {page_num + 1}...", end=" ")
            tables = page.extract_tables()
            
            if tables:
                for table in tables:
                    if len(table) >= 3 and len(table[2]) >= 11:
                        data_row = table[2]
                        
                        col_shlok_num = [x.strip() for x in str(data_row[1]).split('\n') if x.strip()]
                        col_chapter = [x.strip() for x in str(data_row[2]).split('\n') if x.strip()]
                        col_chapter_name = [x.strip() for x in str(data_row[3]).split('\n') if x.strip()]
                        col_keywords = [x.strip() for x in str(data_row[4]).split('\n') if x.strip()]
                        col_theme = [x.strip() for x in str(data_row[5]).split('\n') if x.strip()]
                        col_speaker = [x.strip() for x in str(data_row[6]).split('\n') if x.strip()]
                        col_summary = [x.strip() for x in str(data_row[7]).split('\n') if x.strip()]
                        col_ref = [x.strip() for x in str(data_row[8]).split('\n') if x.strip()]
                        col_link = [x.strip() for x in str(data_row[9]).split('\n') if x.strip()]
                        col_star = [x.strip() for x in str(data_row[10]).split('\n') if x.strip()]
                        
                        num_shloks = len(col_shlok_num)
                        
                        for i in range(num_shloks):
                            try:
                                shlok_num = int(col_shlok_num[i]) if i < len(col_shlok_num) else 0
                                chapter = int(col_chapter[i]) if i < len(col_chapter) else 0
                                
                                if shlok_num == 0 or chapter == 0:
                                    continue
                                
                                shlok = {
                                    "": "",
                                    "__1": chapter,
                                    "__2": col_chapter_name[i] if i < len(col_chapter_name) else "",
                                    "__3": shlok_num,
                                    "__4": col_keywords[i] if i < len(col_keywords) else "",
                                    "__5": int(col_star[i]) if i < len(col_star) and col_star[i].isdigit() else 0,
                                    "__6": col_theme[i] if i < len(col_theme) else "",
                                    "__7": col_speaker[i] if i < len(col_speaker) else "",
                                    "__8": col_summary[i] if i < len(col_summary) else "",
                                    "__9": col_link[i] if i < len(col_link) else ""
                                }
                                
                                shloks.append(shlok)
                            except:
                                pass
            print("✓")
    
    print(f"\nTotal shloks extracted: {len(shloks)}")
    
    header = {
        "": "",
        "__1": "Chapter #",
        "__2": "Chapter Name",
        "__3": "Shlok #",
        "__4": "Keywords",
        "__5": "Star",
        "__6": "Theme",
        "__7": "Speaker",
        "__8": "Shlok Summary",
        "__9": "AV Link"
    }
    
    shloks.insert(0, header)
    
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(shloks, f, ensure_ascii=False, indent=2)
    
    print(f"✓ Hindi shloks saved to: {output_path}")
    print(f"File size: {Path(output_path).stat().st_size / 1024:.2f} KB")
    
    if len(shloks) > 1:
        print(f"\nSample shlok (index 1):")
        sample = shloks[1]
        print(f"  Chapter: {sample['__1']}, Shlok: {sample['__3']}")
        print(f"  Summary: {sample['__8'][:80]}...")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
