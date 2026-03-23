"""
FIXED extraction script - handle multiple data rows in each table.
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
    162: 'ृ', 163: 'ज्ञ', 200: 'ष', 205: 'छ', 215: 'य', 218: 'ध', 
    219: 'य', 220: 'ण', 222: 'थ', 224: 'र', 229: 'त', 230: 'ध', 
    231: 'य', 232: 'म', 272: 'द', 287: '्', 292: 'र', 302: 'ष',
    467: 'श्र', 506: 'ढ़', 509: 'क्ष', 547: 'य', 
    585: 'क', 622: 'ध', 871: 'व', 872: 'ब', 873: 'य', 874: 'व', 876: 'ध',
    1: 'अ', 2: 'आ', 3: 'इ', 4: 'ई', 5: 'उ', 6: 'ऊ', 7: 'ऋ', 
    8: 'ए', 9: 'ऐ', 10: 'ओ', 44: 'औ',
    11: 'क', 12: 'ख', 13: 'ग', 14: 'घ',
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
    
    for wrong, right in CORRECTIONS.items():
        text = text.replace(wrong, right)
    
    def replace_cid(m):
        cid = int(m.group(1))
        return CID_MAP.get(cid, f"[cid:{cid}]")
    
    return re.sub(r'\(cid:(\d+)\)', replace_cid, text).strip()

def split_cell(cell):
    """Split cell by newlines."""
    if not cell:
        return []
    return [line.strip() for line in str(cell).split('\n') if line.strip()]

def extract_shloks():
    """Extract shloks from ALL data rows in tables, not just row 2."""
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
                
                # Process ALL data rows (not just row 2)
                # Row 0 and 1 are headers, row 2+ are data
                for row_idx in range(2, len(table)):
                    row = table[row_idx]
                    if len(row) < 11:
                        continue
                    
                    # Extract columns
                    vs = split_cell(row[1])
                    cs = split_cell(row[2])
                    ns = split_cell(row[3])
                    ts = split_cell(row[5])
                    ss = split_cell(row[6])
                    ms = split_cell(row[7])
                    ls = split_cell(row[9])
                    zs = split_cell(row[10]) if len(row) > 10 else []
                    
                    # Create entries
                    for i in range(max(len(vs), len(cs), len(ns))):
                        try:
                            v = int(vs[i]) if i < len(vs) else 0
                            c = int(cs[i]) if i < len(cs) else 0
                            if v == 0 or c == 0:
                                continue
                            
                            data.append({
                                "": "",
                                "__1": c,
                                "__2": fix_text(ns[i]) if i < len(ns) else "",
                                "__3": v,
                                "__4": "",
                                "__5": int(zs[i]) if i < len(zs) and zs[i].isdigit() else 0,
                                "__6": fix_text(ts[i]) if i < len(ts) else "",
                                "__7": fix_text(ss[i]) if i < len(ss) else "",
                                "__8": fix_text(ms[i]) if i < len(ms) else "",
                                "__9": ls[i] if i < len(ls) else ""
                            })
                        except:
                            pass
    
    return data

if __name__ == "__main__":
    print("Extracting Hindi shloks from ALL table rows...")
    data = extract_shloks()
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Extracted {len(data)-1} shloks")
    print(f"✅ Saved to {output_path}")
