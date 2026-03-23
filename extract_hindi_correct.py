"""
CORRECTED extraction script - properly map all 18 columns from Hindi PDF.

Column mapping (18 columns in Hindi PDF):
  Col 0: Empty
  Col 1: Verse number (repeats for multi-line)
  Col 2: Chapter number (all same for one chapter)
  Col 3: Chapter name
  Col 4: Verse number (again)
  Col 5-11: Keywords/themes (7 keyword columns)
  Col 12: Verse reference (1.1, 1.2, etc.)
  Col 13: Video file (001 1.1.mp4, etc.)
  Col 14: Star rating (1-5)
  Col 15: Theme
  Col 16: Speaker
  Col 17: Summary
"""

import pdfplumber
import json
import re

pdf_path = r"D:\zita\Vita\SriMadBhagvadGita Reels _ Shorts _ Keywords & Links _ HINDI - Hindi Table.pdf"
output_path = r"D:\zita\Vita\assets\json\shlok_data_hindi.json"

# CID-to-character mapping
CID_MAP = {
    50: '्', 51: 'ं', 52: 'ः', 53: '़',
    81: 'ा', 82: 'ि', 83: 'ी', 91: 'ु', 92: 'ू', 93: 'ृ', 94: 'ॄ', 
    95: 'ॅ', 96: 'े', 97: 'ै', 98: 'ॉ', 99: 'ो', 100: 'ौ',
    15: 'ङ', 16: 'च', 17: 'छ', 18: 'ज', 19: 'झ', 20: 'ञ',
    21: 'ट', 22: 'ठ', 23: 'ड', 24: 'ढ', 25: 'ण', 26: 'त',
    27: 'थ', 28: 'द', 29: 'ध', 30: 'न', 31: 'प', 32: 'फ',
    33: 'ब', 34: 'भ', 35: 'म', 36: 'य', 37: 'र', 38: 'ल',
    39: 'व', 40: 'श', 41: 'ष', 42: 'स', 43: 'ह',
    46: 'ष', 162: 'ृ', 163: 'ज्ञ', 200: 'ष', 205: 'छ', 215: 'य', 218: 'ध', 
    219: 'य', 220: 'ण', 222: 'थ', 224: 'र', 229: 'त', 230: 'ध', 
    231: 'य', 232: 'म', 272: 'द', 282: 'त्र', 287: '्', 292: 'र', 294: 'त्र', 302: 'ष',
    467: 'न', 506: 'ड़', 509: 'क्ष', 547: 'ी', 
    574: 'य', 585: 'क', 622: 'ध', 871: 'म', 872: 'व', 873: 'य', 874: 'व', 876: 'ध',
    1: 'अ', 2: 'आ', 3: 'इ', 4: 'ई', 5: 'उ', 6: 'ऊ', 7: 'ऋ', 
    8: 'ए', 9: 'ऐ', 10: 'ओ', 44: 'औ',
    11: 'क', 12: 'ख', 13: 'ग', 14: 'घ',
}

KNOWN_CORRECTIONS = {
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
    
    # Apply known corrections first
    for wrong, right in KNOWN_CORRECTIONS.items():
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
    """Extract shloks with correct column mapping."""
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
                
                # Process ALL data rows (starting from row 2)
                for row_idx in range(2, len(table)):
                    row = table[row_idx]
                    if len(row) < 18:  # Need at least 18 columns
                        continue
                    
                    # Extract columns with proper mapping
                    # Col 1: Verse number, Col 2: Chapter, Col 4: Verse num (use as primary)
                    vs_cells = split_cell(row[1])     # Verse number
                    cs_cells = split_cell(row[2])     # Chapter number
                    
                    # Col 5-11: Keywords (7 columns)
                    keywords_cols = [row[5], row[6], row[7], row[8], row[9], row[10], row[11]]
                    
                    # Col 12: Verse ref (1.1, 1.2, etc)
                    verse_ref = split_cell(row[12])   
                    
                    # Col 13: Video link
                    video_cells = split_cell(row[13])
                    
                    # Col 14: Star rating
                    star_cells = split_cell(row[14])
                    
                    # Col 15: Theme
                    theme_cells = split_cell(row[15])
                    
                    # Col 16: Speaker
                    speaker_cells = split_cell(row[16])
                    
                    # Col 17: Summary
                    summary_cells = split_cell(row[17])
                    
                    # Determine how many entries in this row
                    max_entries = max(len(vs_cells), len(cs_cells), 1)
                    
                    # Create entries
                    for i in range(max_entries):
                        try:
                            # Get values with fallback
                            v = int(vs_cells[i]) if i < len(vs_cells) and vs_cells[i].isdigit() else 0
                            c = int(cs_cells[i]) if i < len(cs_cells) and cs_cells[i].isdigit() else 0
                            
                            # Skip if no chapter or verse
                            if v == 0 or c == 0:
                                continue
                            
                            # Extract keywords from all 7 keyword columns
                            keywords = []
                            for kw_col in keywords_cols:
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
                                "__2": fix_text(theme_cells[i]) if i < len(theme_cells) else "",
                                "__3": v,
                                "__4": " ".join(keywords),  # Keywords from columns 5-11
                                "__5": star,               # Star from column 14
                                "__6": fix_text(verse_ref[i]) if i < len(verse_ref) else "",
                                "__7": fix_text(speaker_cells[i]) if i < len(speaker_cells) else "",
                                "__8": fix_text(summary_cells[i]) if i < len(summary_cells) else "",
                                "__9": video_cells[i] if i < len(video_cells) else ""
                            }
                            
                            data.append(entry)
                            
                        except Exception as e:
                            print(f"Error processing row {row_idx}, entry {i}: {e}")
                            continue
    
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
    for idx in [1, 2, 50, 100, 200]:
        if idx < len(data):
            entry = data[idx]
            print(f"\nEntry {idx}:")
            print(f"  Chapter {entry['__1']}, Verse {entry['__3']}")
            print(f"  Theme: {entry['__2']}")
            print(f"  Keywords (__4): {entry['__4']}")
            print(f"  Star (__5): {entry['__5']}")
