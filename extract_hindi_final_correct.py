"""
FINAL CORRECT extraction script with proper column mapping.

CORRECT MAPPING (from PDF analysis):
  Col 1: Verse number
  Col 2: Chapter number  
  Col 3: Chapter name/title (अर्जुन विषाद योग) → __2
  Col 4: Verse number (duplicate)
  Col 5-11: Keywords (7 columns) → __4
  Col 12: Verse reference (1.1, 1.2) → NOT USED
  Col 13: Video link (001 1.1.mp4) → __9
  Col 14: Star rating (1-5) → __5
  Col 15: Theme (रणनीति) → __6
  Col 16: Speaker (धृतराष्ट्र, संजय) → __7
  Col 17: Summary → __8
"""

import pdfplumber
import json
import re

pdf_path = r"D:\zita\Vita\SriMadBhagvadGita Reels _ Shorts _ Keywords & Links _ HINDI - Hindi Table.pdf"
output_path = r"D:\zita\Vita\assets\json\shlok_data_hindi.json"

# Extended CID-to-character mapping
CID_MAP = {
    1: 'अ', 2: 'आ', 3: 'इ', 4: 'ई', 5: 'उ', 6: 'ऊ', 7: 'ऋ', 8: 'ए', 9: 'ऐ', 10: 'ओ', 44: 'औ',
    11: 'क', 12: 'ख', 13: 'ग', 14: 'घ', 15: 'ङ', 16: 'च', 17: 'छ', 18: 'ज', 19: 'झ', 20: 'ञ',
    21: 'ट', 22: 'ठ', 23: 'ड', 24: 'ढ', 25: 'ण', 26: 'त', 27: 'थ', 28: 'द', 29: 'ध', 30: 'न',
    31: 'प', 32: 'फ', 33: 'ब', 34: 'भ', 35: 'म', 36: 'य', 37: 'र', 38: 'ल', 39: 'व', 40: 'श',
    41: 'ष', 42: 'स', 43: 'ह',
    50: '्', 51: 'ं', 52: 'ः', 53: '़',
    81: 'ा', 82: 'ि', 83: 'ी', 91: 'ु', 92: 'ू', 93: 'ृ', 94: 'ॄ', 95: 'ॅ', 96: 'े', 97: 'ै', 98: 'ॉ', 99: 'ो', 100: 'ौ',
    162: 'ृ', 163: 'ज्ञ', 200: 'ष', 205: 'छ', 215: 'य', 218: 'ध', 219: 'य', 220: 'ण', 222: 'थ',
    224: 'र', 229: 'त', 230: 'ध', 231: 'य', 232: 'म', 272: 'द', 282: 'त्र', 287: '्', 292: 'र',
    294: 'त्र', 302: 'ष', 419: 'र', 465: 'न', 467: 'न', 506: 'ड़', 509: 'क्ष', 547: 'ी', 568: 'क',
    574: 'य', 581: 'त', 585: 'क', 622: 'ध', 871: 'म', 872: 'व', 873: 'य', 874: 'व', 876: 'ध',
}

CORRECTIONS = {
    'अजुन(cid:91) (cid:874)वषाद योग': 'अर्जुन विषाद योग',
    'धम(cid:162)(cid:91) े(cid:287)': 'धर्मक्षेत्र',
    'कु(cid:509)(cid:162)े(cid:287)': 'कुरुक्षेत्र',
    'मो(cid:162) सं(cid:219)यास योग': 'मोक्ष संन्यास योग',
}

def fix_text(text):
    """Fix Hindi text with CID replacements."""
    if not text:
        return ""
    
    text = str(text)
    
    # Apply known corrections
    for wrong, right in CORRECTIONS.items():
        text = text.replace(wrong, right)
    
    # Replace CID codes
    def replace_cid(m):
        cid = int(m.group(1))
        return CID_MAP.get(cid, f"[cid:{cid}]")
    
    return re.sub(r'\(cid:(\d+)\)', replace_cid, text).strip()

def split_cell(cell):
    """Split cell by newlines, return list of non-empty strings."""
    if not cell:
        return []
    return [line.strip() for line in str(cell).split('\n') if line.strip()]

def extract_shloks():
    """Extract shloks with CORRECT column mapping."""
    data = [{
        "": "",
        "__1": "Chapter #", "__2": "Chapter Name", "__3": "Shlok #",
        "__4": "Keywords", "__5": "Star", "__6": "Theme",
        "__7": "Speaker", "__8": "Shlok Summary", "__9": "AV Link"
    }]
    
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            tables = page.extract_tables()
            if not tables:
                continue
            
            for table in tables:
                if len(table) < 3:
                    continue
                
                row = table[2]
                if len(row) < 18:
                    continue
                
                # Extract columns with CORRECT mapping
                vs_cells = split_cell(row[1])      # Col 1: Verse numbers
                cs_cells = split_cell(row[2])      # Col 2: Chapter numbers
                
                # __2: Chapter name from Col 3
                title_cells = split_cell(row[3])
                
                # __4: Keywords from Col 5-11 (7 keyword columns)
                keyword_cols = [row[5], row[6], row[7], row[8], row[9], row[10], row[11]]
                
                # __5: Star rating from Col 14
                star_cells = split_cell(row[14])
                
                # __6: Theme from Col 15
                theme_cells = split_cell(row[15])
                
                # __7: Speaker from Col 16
                speaker_cells = split_cell(row[16])
                
                # __8: Summary from Col 17
                summary_cells = split_cell(row[17])
                
                # __9: Video link from Col 13
                link_cells = split_cell(row[13])
                
                # Determine how many entries in this row
                max_entries = max(len(vs_cells), len(cs_cells), 1)
                
                # Create entries
                for i in range(max_entries):
                    try:
                        v = int(vs_cells[i]) if i < len(vs_cells) and vs_cells[i].isdigit() else 0
                        c = int(cs_cells[i]) if i < len(cs_cells) and cs_cells[i].isdigit() else 0
                        
                        if v == 0 or c == 0:
                            continue
                        
                        # Extract keywords from all 7 keyword columns
                        keywords = []
                        for kw_col in keyword_cols:
                            kw_cells = split_cell(kw_col)
                            if i < len(kw_cells) and kw_cells[i]:
                                keywords.append(fix_text(kw_cells[i]))
                        
                        # Get star rating
                        star = 0
                        if i < len(star_cells):
                            try:
                                star = int(star_cells[i])
                                if star < 0 or star > 5:
                                    star = 0
                            except:
                                star = 0
                        
                        entry = {
                            "": "",
                            "__1": c,
                            "__2": fix_text(title_cells[i]) if i < len(title_cells) else "",
                            "__3": v,
                            "__4": " ".join(keywords),
                            "__5": star,
                            "__6": fix_text(theme_cells[i]) if i < len(theme_cells) else "",
                            "__7": fix_text(speaker_cells[i]) if i < len(speaker_cells) else "",
                            "__8": fix_text(summary_cells[i]) if i < len(summary_cells) else "",
                            "__9": link_cells[i] if i < len(link_cells) else ""
                        }
                        
                        data.append(entry)
                        
                    except Exception as e:
                        pass
    
    return data

if __name__ == "__main__":
    print("Extracting Hindi shloks with CORRECT column mapping...")
    data = extract_shloks()
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Extracted {len(data)-1} shloks")
    print(f"✅ Saved to {output_path}")
    
    # Print sample entries for verification
    print("\n=== SAMPLE ENTRIES ===")
    for idx in [1, 2, 50]:
        if idx < len(data):
            entry = data[idx]
            print(f"\nEntry {idx}:")
            print(f"  __2 (Title): {entry['__2']}")
            print(f"  __6 (Theme): {entry['__6']}")
            print(f"  __7 (Speaker): {entry['__7']}")
            print(f"  __4 (Keywords): {entry['__4'][:60]}...")
