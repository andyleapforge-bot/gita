"""
Extract Hindi shlok data from PDF with proper Unicode encoding.
This script attempts multiple approaches to handle the embedded font CID issues.
"""

import pdfplumber
import json
import re
from pathlib import Path

pdf_path = r"D:\zita\Vita\SriMadBhagvadGita Reels _ Shorts _ Keywords & Links _ HINDI - Hindi Table.pdf"
output_path = r"D:\zita\Vita\assets\json\shlok_data_hindi.json"
debug_output = r"D:\zita\Vita\pdf_extraction_debug.txt"

# Common CID to Devanagari character mappings (based on common PDF fonts)
# This is a partial mapping - we'll try to identify patterns
cid_mapping = {
    91: 'ु',      # vowel sign u
    162: 'ृ',     # vowel sign ri
    163: 'ज्ञ',   # ja-nya
    167: 'ा',     # vowel sign aa
    287: '्',     # virama
    467: 'श्र',   # shra
    509: 'क्ष',   # ksha
    547: 'य',     # ya
    874: 'व',     # va
}

def clean_text_with_cid(text):
    """
    Clean text by replacing CID codes with proper Unicode characters.
    """
    if not text:
        return ""
    
    # Replace (cid:XXX) patterns
    def replace_cid(match):
        cid_num = int(match.group(1))
        if cid_num in cid_mapping:
            return cid_mapping[cid_num]
        return match.group(0)  # Keep original if not in mapping
    
    cleaned = re.sub(r'\(cid:(\d+)\)', replace_cid, text)
    return cleaned.strip()

def extract_hindi_data():
    """
    Extract Hindi shlok data from PDF.
    """
    shloks = []
    debug_info = []
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            debug_info.append(f"Total pages: {len(pdf.pages)}\n")
            
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
            
            for page_num, page in enumerate(pdf.pages):
                debug_info.append(f"\n=== Processing page {page_num + 1} ===")
                tables = page.extract_tables()
                
                if not tables:
                    debug_info.append("No tables found")
                    continue
                
                debug_info.append(f"Found {len(tables)} table(s)")
                
                for table_idx, table in enumerate(tables):
                    debug_info.append(f"\nTable {table_idx}: {len(table)} rows, {len(table[0]) if table else 0} cols")
                    
                    # Skip header rows (usually first 2-3 rows)
                    for row_idx, row in enumerate(table):
                        if row_idx < 2:  # Skip header rows
                            continue
                        
                        if len(row) < 10:
                            debug_info.append(f"  Row {row_idx}: Skipped (only {len(row)} columns)")
                            continue
                        
                        # Debug: show raw data from first few rows
                        if row_idx < 5:
                            debug_info.append(f"\n  Row {row_idx} RAW:")
                            for col_idx, cell in enumerate(row[:10]):
                                preview = str(cell)[:60] if cell else ""
                                debug_info.append(f"    Col {col_idx}: {preview}")
                        
                        # Extract columns
                        try:
                            # Handle multi-line cells by taking first line or joining
                            def get_cell_text(cell_idx):
                                cell = row[cell_idx] if cell_idx < len(row) else ""
                                if not cell:
                                    return ""
                                cell_str = str(cell)
                                # Split by newlines and take parts
                                lines = [l.strip() for l in cell_str.split('\n') if l.strip()]
                                return '\n'.join(lines) if lines else ""
                            
                            # Column mapping (adjust based on actual PDF structure)
                            shlok_num_text = get_cell_text(1)
                            chapter_text = get_cell_text(2)
                            chapter_name = get_cell_text(3)
                            keywords = get_cell_text(4)
                            theme = get_cell_text(5)
                            speaker = get_cell_text(6)
                            summary = get_cell_text(7)
                            ref = get_cell_text(8)
                            link = get_cell_text(9)
                            star_text = get_cell_text(10) if len(row) > 10 else "0"
                            
                            # Parse numeric fields
                            try:
                                shlok_num = int(shlok_num_text.split('\n')[0]) if shlok_num_text else 0
                            except:
                                shlok_num = 0
                            
                            try:
                                chapter = int(chapter_text.split('\n')[0]) if chapter_text else 0
                            except:
                                chapter = 0
                            
                            try:
                                star = int(star_text.split('\n')[0]) if star_text else 0
                            except:
                                star = 0
                            
                            # Skip invalid entries
                            if shlok_num == 0 or chapter == 0:
                                continue
                            
                            # Clean text with CID codes
                            shlok = {
                                "": "",
                                "__1": chapter,
                                "__2": clean_text_with_cid(chapter_name),
                                "__3": shlok_num,
                                "__4": keywords,
                                "__5": star,
                                "__6": clean_text_with_cid(theme),
                                "__7": clean_text_with_cid(speaker),
                                "__8": clean_text_with_cid(summary),
                                "__9": link
                            }
                            
                            shloks.append(shlok)
                            
                            if row_idx < 5:
                                debug_info.append(f"  Row {row_idx} PARSED: Ch={chapter}, Verse={shlok_num}, Theme={shlok['__6']}")
                        
                        except Exception as e:
                            debug_info.append(f"  Error parsing row {row_idx}: {str(e)}")
        
        debug_info.append(f"\n\nTotal shloks extracted: {len(shloks) - 1}")  # -1 for header
        
    except Exception as e:
        debug_info.append(f"ERROR: {str(e)}")
    
    # Write debug output
    with open(debug_output, 'w', encoding='utf-8') as f:
        f.write('\n'.join(debug_info))
    
    print('\n'.join(debug_info[-20:]))  # Print last 20 lines
    
    return shloks

if __name__ == "__main__":
    print("Extracting Hindi PDF with proper encoding handling...")
    shloks = extract_hindi_data()
    
    # Save to JSON
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(shloks, f, ensure_ascii=False, indent=2)
    
    print(f"\nSaved {len(shloks) - 1} shloks to {output_path}")
    print(f"Debug output saved to {debug_output}")
