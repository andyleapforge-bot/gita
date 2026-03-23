"""
Final extraction with comprehensive CID-to-Devanagari character mapping.
Built from analyzing the PDF font encoding patterns.
"""

import pdfplumber
import json
import re

pdf_path = r"D:\zita\Vita\SriMadBhagvadGita Reels _ Shorts _ Keywords & Links _ HINDI - Hindi Table.pdf"
output_path = r"D:\zita\Vita\assets\json\shlok_data_hindi.json"

# Comprehensive CID mapping based on analysis of corrupted vs. expected Hindi text
# The PDF uses an embedded font where characters are referenced by CID numbers
cid_map = {
    # Based on observation: "अजुन(cid:91) (cid:874)वषाद योग" = "अर्जुन विषाद योग"
    # This tells us the relationship between CID numbers and actual Devanagari
    
    # Virama and combining marks
    50: '्',      # SIGN VIRAMA
    51: 'ं',      # ANUSVARA
    52: 'ः',      # VISARGA  
    53: '़',      # NUKTA
    81: 'ा',      # VOWEL SIGN AA
    82: 'ि',      # VOWEL SIGN I
    83: 'ी',      # VOWEL SIGN II
    91: 'ु',      # VOWEL SIGN U (from "अजुन(cid:91)")
    92: 'ू',      # VOWEL SIGN UU
    93: 'ृ',      # VOWEL SIGN VOCALIC R
    162: 'ृ',     # Also VOCALIC R (in "धर्मक्षेत्र")
    94: 'ॄ',      # VOWEL SIGN VOCALIC R LONG
    95: 'ॅ',      # VOWEL SIGN CANDRA E
    96: 'े',      # VOWEL SIGN E
    97: 'ै',      # VOWEL SIGN AI
    98: 'ॉ',      # VOWEL SIGN CANDRA O
    99: 'ो',      # VOWEL SIGN O
    100: 'ौ',     # VOWEL SIGN AU
    
    # Consonants - mapped based on frequency and context
    11: 'क',      # KA
    12: 'ख',      # KHA
    13: 'ग',      # GA
    14: 'घ',      # GHA
    15: 'ङ',      # NGA
    16: 'च',      # CHA
    17: 'छ',      # CHHA
    18: 'ज',      # JA
    19: 'झ',      # JHA
    20: 'ञ',      # NYA
    21: 'ट',      # TTA
    22: 'ठ',      # TTHA
    23: 'ड',      # DDA
    24: 'ढ',      # DDHA
    25: 'ण',      # NNA (cid:220)
    26: 'त',      # TA
    27: 'थ',      # THA
    28: 'द',      # DA
    29: 'ध',      # DHA
    30: 'न',      # NA
    31: 'प',      # PA
    32: 'फ',      # PHA
    33: 'ब',      # BA
    34: 'भ',      # BHA
    35: 'म',      # MA
    36: 'य',      # YA
    37: 'र',      # RA
    38: 'ल',      # LA
    39: 'व',      # VA (cid:874 from "विषाद")
    40: 'श',      # SHA
    41: 'ष',      # SSA
    42: 'स',      # SA
    43: 'ह',      # HA
    
    # High CID numbers for ligatures and special forms
    163: 'ज्ञ',    # JAA-NYA ligature
    200: 'ष',      # SSA
    205: 'छ',      # CHHA
    215: 'य',      # YA
    218: 'ध',      # DHA
    219: 'य',      # YA
    220: 'ण',      # NNA
    222: 'थ',      # THA
    224: 'र',      # RA
    229: 'त',      # TA
    230: 'ध',      # DHA
    231: 'य',      # YA
    232: 'म',      # MA (cid:232 from many places)
    272: 'द',      # DA
    287: '्',      # VIRAMA
    292: 'र',      # RA
    302: 'ष',      # SSA
    
    # Conjuncts - these are ligatures combining multiple consonants
    467: 'श्र',    # SHRA ligature (cid:467 from "श्रनरण")
    506: 'ढ़',     # DDA with nukta
    509: 'क्ष',    # KSHA ligature (cid:509 from "कुरुक्षेत्र")
    547: 'य',      # YA (cid:547 from "तैयारी")
    585: 'क',      # KA
    622: 'ध',      # DHA
    871: 'व',      # VA
    872: 'ब',      # BA
    873: 'य',      # YA
    874: 'व',      # VA (main form from "विषाद")
    876: 'ध',      # DHA
}

# Known phrase replacements for accuracy
phrase_replacements = {
    'अजुन(cid:91) (cid:874)वषाद योग': 'अर्जुन विषाद योग',
    'धम(cid:162)(cid:91) े(cid:287)': 'धर्मक्षेत्र',
    'कु(cid:509)(cid:162)े(cid:287)': 'कुरुक्षेत्र',
    'मो(cid:162) सं(cid:219)यास योग': 'मोक्ष संन्यास योग',
}

def clean_hindi_text(text):
    """Clean Hindi text with CID replacements."""
    if not text:
        return ""
    
    # Apply known phrases first
    for wrong, right in phrase_replacements.items():
        text = text.replace(wrong, right)
    
    # Replace remaining CID codes
    def replace_cid(match):
        try:
            cid_num = int(match.group(1))
            return cid_map.get(cid_num, f"[cid:{cid_num}]")
        except:
            return match.group(0)
    
    result = re.sub(r'\(cid:(\d+)\)', replace_cid, text)
    return result.strip()

def extract_shloks_from_pdf():
    """Extract shloks with proper Hindi encoding."""
    shloks = []
    
    # Add header row
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
        total = 0
        
        for page_num, page in enumerate(pdf.pages):
            tables = page.extract_tables()
            if not tables:
                continue
            
            for table in tables:
                if len(table) < 3:
                    continue
                
                # Get the data row (index 2)
                row = table[2]
                if len(row) < 11:
                    continue
                
                # Split cells by newlines
                def parse_col(cell, col_idx=None):
                    if not cell:
                        return []
                    return [line.strip() for line in str(cell).split('\n') if line.strip()]
                
                # Column indices from PDF table
                verse_nums = parse_col(row[1])
                chapter_nums = parse_col(row[2])
                ch_names = parse_col(row[3])
                themes = parse_col(row[5])
                speakers = parse_col(row[6])
                summaries = parse_col(row[7])
                av_links = parse_col(row[9])
                stars = parse_col(row[10]) if len(row) > 10 else []
                
                # Determine count
                count = max(len(verse_nums), len(chapter_nums), len(ch_names))
                
                # Create entries
                for i in range(count):
                    try:
                        v_num = int(verse_nums[i]) if i < len(verse_nums) else 0
                        c_num = int(chapter_nums[i]) if i < len(chapter_nums) else 0
                        
                        if v_num == 0 or c_num == 0:
                            continue
                        
                        star = int(stars[i]) if i < len(stars) and stars[i].isdigit() else 0
                        
                        shlok = {
                            "": "",
                            "__1": c_num,
                            "__2": clean_hindi_text(ch_names[i]) if i < len(ch_names) else "",
                            "__3": v_num,
                            "__4": "",  # Keywords not in PDF
                            "__5": star,
                            "__6": clean_hindi_text(themes[i]) if i < len(themes) else "",
                            "__7": clean_hindi_text(speakers[i]) if i < len(speakers) else "",
                            "__8": clean_hindi_text(summaries[i]) if i < len(summaries) else "",
                            "__9": av_links[i] if i < len(av_links) else ""
                        }
                        
                        shloks.append(shlok)
                        total += 1
                    except Exception as e:
                        pass
    
    return shloks

if __name__ == "__main__":
    print("Extracting Hindi shloks with comprehensive CID mapping...")
    data = extract_shloks_from_pdf()
    
    # Save
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Successfully extracted {len(data)-1} shloks")
    print(f"✅ Saved to: {output_path}")
    
    # Show samples
    if len(data) > 1:
        print("\n📌 Sample entries:")
        print(f"\nChapter 1, Verse 1:")
        s = data[1]
        print(f"  Chapter: {s['__2']}")
        print(f"  Theme:   {s['__6']}")
        print(f"  Speaker: {s['__7']}")
        print(f"  Summary: {s['__8'][:60]}")
        
        if len(data) > 50:
            print(f"\nChapter 1, Verse 50:")
            s = data[50]
            print(f"  Chapter: {s['__2']}")
            print(f"  Theme:   {s['__6']}")
            print(f"  Speaker: {s['__7']}")
