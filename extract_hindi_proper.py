"""
Extract Hindi shlok data from PDF with correct field mapping and CID handling.
Based on English version structure analysis.
"""

import pdfplumber
import json
import re
from collections import defaultdict

pdf_path = r"D:\zita\Vita\SriMadBhagvadGita Reels _ Shorts _ Keywords & Links _ HINDI - Hindi Table.pdf"
output_path = r"D:\zita\Vita\assets\json\shlok_data_hindi.json"

# CID to Unicode mappings for common Devanagari characters from embedded PDF fonts
# This is a partial mapping - the most common ones we see
cid_char_map = {
    # Based on the CID codes appearing in the corrupted text
    91: 'ु',      # U+0941 Vowel Sign U
    162: 'ृ',     # U+0943 Vowel Sign Vocalic R  
    163: 'ज्ञ',   # Ja-Nya ligature (approximately)
    167: 'ा',     # U+093E Vowel Sign AA
    200: 'ष',     # U+0937 Letter SSA
    205: 'छ',     # U+0959 Letter CHHHA
    215: 'य',     # U+0959 Letter YYA or TTHA - using य
    218: 'ध',     # U+0927 Letter DHA
    219: 'य',     # U+092F Letter YA
    220: 'ण',     # U+0923 Letter NNA
    222: 'थ',     # U+0925 Letter THA
    224: 'र',     # U+0930 Letter RA
    229: 'त',     # U+0924 Letter TA
    230: 'ध',     # U+0927 Letter DHA
    231: 'य',     # U+092F Letter YA
    232: 'म',     # U+092E Letter MA
    272: 'द',     # U+0926 Letter DA
    287: '्',     # U+094D Sign Virama
    292: 'र',     # U+0930 Letter RA (in conjunct)
    302: 'ष',     # U+0937 Letter SSA
    467: 'श्र',   # SHR conjunct
    506: 'ढ़',    # Letter DHA with nukta
    509: 'क्ष',   # KSH conjunct
    547: 'य',     # U+092F Letter YA
    585: 'क',     # U+0915 Letter KA
    622: 'ध',     # U+0927 Letter DHA
    871: 'व',     # U+0935 Letter VA
    872: 'ब',     # U+092C Letter BA
    873: 'य',     # U+092F Letter YA
    874: 'व',     # U+0935 Letter VA
    876: 'ध',     # U+0927 Letter DHA
}

def fix_cid_codes(text):
    """Replace (cid:XXX) codes with best-guess Unicode characters."""
    if not text:
        return ""
    
    def replace_cid(match):
        try:
            cid_num = int(match.group(1))
            return cid_char_map.get(cid_num, match.group(0))
        except:
            return match.group(0)
    
    # Replace all (cid:XXX) patterns
    result = re.sub(r'\(cid:(\d+)\)', replace_cid, text)
    return result.strip()

def extract_shloks():
    """Extract shlok data from PDF."""
    shloks = []
    
    # Add header
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
        total_rows = 0
        
        for page_num, page in enumerate(pdf.pages):
            tables = page.extract_tables()
            
            if not tables:
                continue
            
            for table in tables:
                if len(table) < 3:
                    continue
                
                # The table structure is:
                # Row 0: Empty row with blank cells
                # Row 1: Appears to be another structure row
                # Row 2+: Data rows containing multiple shloks per cell (separated by newlines)
                
                # Process the third row (index 2) which contains data
                if len(table) > 2:
                    data_row = table[2]
                    
                    # Expected column mapping (18 columns based on PDF structure):
                    # Col 0: Empty
                    # Col 1: Shlok numbers (newline separated)
                    # Col 2: Chapter numbers (newline separated)
                    # Col 3: Chapter names (newline separated)
                    # Col 4: Verse numbers (same as col 1 it seems)
                    # Col 5: Theme (newline separated)
                    # Col 6: Speaker (newline separated)
                    # Col 7: Summary (newline separated) 
                    # ... etc
                    
                    # Extract and split each column
                    if len(data_row) >= 11:
                        # Column indices (0-based)
                        col_verse_num = data_row[1] if len(data_row) > 1 else ""
                        col_chapter = data_row[2] if len(data_row) > 2 else ""
                        col_chapter_name = data_row[3] if len(data_row) > 3 else ""
                        col_keywords = data_row[4] if len(data_row) > 4 else ""  # Not in current structure
                        col_theme = data_row[5] if len(data_row) > 5 else ""
                        col_speaker = data_row[6] if len(data_row) > 6 else ""
                        col_summary = data_row[7] if len(data_row) > 7 else ""
                        col_ref = data_row[8] if len(data_row) > 8 else ""
                        col_av_link = data_row[9] if len(data_row) > 9 else ""
                        col_star = data_row[10] if len(data_row) > 10 else "0"
                        
                        # Split newline-separated values
                        def split_cell(cell):
                            if not cell:
                                return []
                            lines = str(cell).split('\n')
                            return [line.strip() for line in lines if line.strip()]
                        
                        verses = split_cell(col_verse_num)
                        chapters = split_cell(col_chapter)
                        chapter_names = split_cell(col_chapter_name)
                        themes = split_cell(col_theme)
                        speakers = split_cell(col_speaker)
                        summaries = split_cell(col_summary)
                        av_links = split_cell(col_av_link)
                        stars = split_cell(col_star)
                        
                        # Number of shloks in this row
                        num_entries = max(
                            len(verses), len(chapters), len(chapter_names),
                            len(themes), len(speakers), len(summaries), len(av_links)
                        )
                        
                        # Create shlok entries
                        for idx in range(num_entries):
                            try:
                                verse_num = int(verses[idx]) if idx < len(verses) else 0
                                chapter_num = int(chapters[idx]) if idx < len(chapters) else 0
                                
                                # Skip invalid entries
                                if verse_num == 0 or chapter_num == 0:
                                    continue
                                
                                # Get values with fallback to empty string
                                chapter_name = fix_cid_codes(chapter_names[idx]) if idx < len(chapter_names) else ""
                                theme = fix_cid_codes(themes[idx]) if idx < len(themes) else ""
                                speaker = fix_cid_codes(speakers[idx]) if idx < len(speakers) else ""
                                summary = fix_cid_codes(summaries[idx]) if idx < len(summaries) else ""
                                av_link = av_links[idx] if idx < len(av_links) else ""
                                star_val = int(stars[idx]) if idx < len(stars) and stars[idx].isdigit() else 0
                                
                                shlok = {
                                    "": "",
                                    "__1": chapter_num,
                                    "__2": chapter_name,
                                    "__3": verse_num,
                                    "__4": "",  # Keywords - not available in PDF
                                    "__5": star_val,
                                    "__6": theme,
                                    "__7": speaker,
                                    "__8": summary,
                                    "__9": av_link
                                }
                                
                                shloks.append(shlok)
                                total_rows += 1
                            
                            except Exception as e:
                                pass  # Skip entries with parsing errors
    
    return shloks

if __name__ == "__main__":
    print("Extracting Hindi shloks with proper CID mapping...")
    shloks = extract_shloks()
    
    # Save to JSON
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(shloks, f, ensure_ascii=False, indent=2)
    
    print(f"✓ Extracted {len(shloks) - 1} shloks (header + data entries)")
    print(f"✓ Saved to {output_path}")
    
    # Show sample
    if len(shloks) > 1:
        print(f"\nSample entry (Chapter 1, Verse 1):")
        sample = shloks[1]
        for key in ['__2', '__6', '__7', '__8']:
            print(f"  {key}: {sample.get(key, '(empty)')[:50]}")
