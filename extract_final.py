"""
Better approach: Extract raw text from PDF and try to recover proper encoding.
Uses the fact that some Hindi characters are rendered correctly while others have CID codes.
"""

import pdfplumber
import json
import re

pdf_path = r"D:\zita\Vita\SriMadBhagvadGita Reels _ Shorts _ Keywords & Links _ HINDI - Hindi Table.pdf"
output_path = r"D:\zita\Vita\assets\json\shlok_data_hindi.json"

# Known mapping based on what we see in the PDF
# From earlier analysis: "अजुन(cid:91) (cid:874)वषाद योग" should be "अर्जुन विषाद योग"
# So: cid:91 = ् (virama), cid:874 = व (va)

# Let's build this from known Hindi text patterns
known_corrections = {
    'अजुन(cid:91) (cid:874)वषाद योग': 'अर्जुन विषाद योग',
    'धम(cid:162)(cid:91) े(cid:287)': 'धर्मक्षेत्र',
    'कु(cid:509)(cid:162)े(cid:287)': 'कुरुक्षेत्र',
    'तैयार(cid:547)': 'तैयारी',  # cid:547 = य
}

# More comprehensive CID mapping based on Devanagari Unicode
cid_mapping_v2 = {
    # Consonants
    11: 'क',    # KA
    12: 'ख',    # KHA
    13: 'ग',    # GA
    14: 'घ',    # GHA
    15: 'ङ',    # NGA
    16: 'च',    # CHA
    17: 'छ',    # CHHA
    18: 'ज',    # JA
    19: 'झ',    # JHA
    20: 'ञ',    # NYA
    21: 'ट',    # TTA
    22: 'ठ',    # TTHA
    23: 'ड',    # DDA
    24: 'ढ',    # DDHA
    25: 'ण',    # NNA
    26: 'त',    # TA
    27: 'थ',    # THA
    28: 'द',    # DA
    29: 'ध',    # DHA
    30: 'न',    # NA
    31: 'प',    # PA
    32: 'फ',    # PHA
    33: 'ब',    # BA
    34: 'भ',    # BHA
    35: 'म',    # MA
    36: 'य',    # YA
    37: 'र',    # RA
    38: 'ल',    # LA
    39: 'व',    # VA
    40: 'श',    # SHA
    41: 'ष',    # SSA
    42: 'स',    # SA
    43: 'ह',    # HA
    
    # Vowels
    1: 'अ',     # A
    2: 'आ',     # AA
    3: 'इ',     # I
    4: 'ई',     # II
    5: 'उ',     # U
    6: 'ऊ',     # UU
    7: 'ऋ',     # VOCALIC R
    8: 'ए',     # E
    9: 'ऐ',     # AI
    10: 'ओ',    # O
    44: 'औ',    # AU
    
    # Vowel signs
    81: 'ा',     # SIGN AA (U+093E)
    82: 'ि',     # SIGN I (U+093F)
    83: 'ी',     # SIGN II (U+0940)
    91: 'ु',     # SIGN U (U+0941)
    92: 'ू',     # SIGN UU (U+0942)
    93: 'ृ',     # SIGN VOCALIC R (U+0943)
    94: 'ॄ',     # SIGN VOCALIC R LONG (U+0944)
    95: 'ॅ',     # SIGN CANDRA E (U+0945)
    96: 'े',     # SIGN E (U+0947)
    97: 'ै',     # SIGN AI (U+0948)
    98: 'ॉ',     # SIGN CANDRA O (U+0949)
    99: 'ो',     # SIGN O (U+094B)
    100: 'ौ',    # SIGN AU (U+094C)
    
    # Virama and other marks
    50: '्',     # SIGN VIRAMA (U+094D)
    51: 'ं',     # SIGN ANUSVARA (U+0902)
    52: 'ः',     # SIGN VISARGA (U+0903)
    53: '़',     # NUKTA (U+093C)
}

def clean_text_smart(text):
    """Clean text by replacing CID codes with Unicode."""
    if not text:
        return ""
    
    # Try known corrections first
    for corrupted, corrected in known_corrections.items():
        text = text.replace(corrupted, corrected)
    
    # Replace remaining CID codes
    def replace_cid(match):
        try:
            cid_num = int(match.group(1))
            return cid_mapping_v2.get(cid_num, match.group(0))
        except:
            return match.group(0)
    
    text = re.sub(r'\(cid:(\d+)\)', replace_cid, text)
    return text.strip()

def extract_from_pdf():
    """Extract from PDF."""
    shloks = []
    
    # Header
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
    shloks.append(header)
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            if not tables:
                continue
            
            for table in tables:
                if len(table) < 3:
                    continue
                
                data_row = table[2]
                if len(data_row) < 11:
                    continue
                
                # Extract columns
                def split_cell(cell):
                    if not cell:
                        return []
                    return [line.strip() for line in str(cell).split('\n') if line.strip()]
                
                verses = split_cell(data_row[1])
                chapters = split_cell(data_row[2])
                chapter_names = split_cell(data_row[3])
                themes = split_cell(data_row[5])
                speakers = split_cell(data_row[6])
                summaries = split_cell(data_row[7])
                av_links = split_cell(data_row[9])
                stars = split_cell(data_row[10]) if len(data_row) > 10 else []
                
                num = max(len(verses), len(chapters), len(chapter_names))
                
                for idx in range(num):
                    try:
                        v = int(verses[idx]) if idx < len(verses) else 0
                        c = int(chapters[idx]) if idx < len(chapters) else 0
                        if v == 0 or c == 0:
                            continue
                        
                        shlok = {
                            "": "",
                            "__1": c,
                            "__2": clean_text_smart(chapter_names[idx]) if idx < len(chapter_names) else "",
                            "__3": v,
                            "__4": "",
                            "__5": int(stars[idx]) if idx < len(stars) and stars[idx].isdigit() else 0,
                            "__6": clean_text_smart(themes[idx]) if idx < len(themes) else "",
                            "__7": clean_text_smart(speakers[idx]) if idx < len(speakers) else "",
                            "__8": clean_text_smart(summaries[idx]) if idx < len(summaries) else "",
                            "__9": av_links[idx] if idx < len(av_links) else ""
                        }
                        shloks.append(shlok)
                    except:
                        pass
    
    return shloks

if __name__ == "__main__":
    print("Extracting with improved mapping...")
    data = extract_from_pdf()
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✓ Extracted {len(data)-1} entries")
    if len(data) > 1:
        print(f"\nSample:")
        for key in '__2 __6 __7 __8'.split():
            print(f"  {key}: {data[1].get(key, '')[:50]}")
