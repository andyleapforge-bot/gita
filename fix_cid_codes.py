"""
Improve CID character mapping and fix encoding issues
"""

import json
import re

# More complete CID mapping based on common Hindi PDF encodings
BETTER_CID_MAP = {
    # Vowels (स्वर)
    1: 'अ', 2: 'आ', 3: 'इ', 4: 'ई', 5: 'उ', 6: 'ऊ', 7: 'ऋ', 8: 'ए', 9: 'ऐ', 10: 'ओ', 44: 'औ',
    # Consonants (व्यंजन)
    11: 'क', 12: 'ख', 13: 'ग', 14: 'घ', 15: 'ङ', 16: 'च', 17: 'छ', 18: 'ज', 19: 'झ', 20: 'ञ',
    21: 'ट', 22: 'ठ', 23: 'ड', 24: 'ढ', 25: 'ण', 26: 'त', 27: 'थ', 28: 'द', 29: 'ध', 30: 'न',
    31: 'प', 32: 'फ', 33: 'ब', 34: 'भ', 35: 'म', 36: 'य', 37: 'र', 38: 'ल', 39: 'व', 40: 'श',
    41: 'ष', 42: 'स', 43: 'ह',
    # Nukta forms
    45: 'ख़', 46: 'ग़', 47: 'ज़', 48: 'ड़', 49: 'ढ़', 50: '्', 51: 'ं', 52: 'ः', 53: '़',
    # Matras (vowel marks)
    81: 'ा', 82: 'ि', 83: 'ी', 91: 'ु', 92: 'ू', 93: 'ृ', 94: 'ॄ', 95: 'ॅ', 96: 'े', 97: 'ै', 98: 'ॉ', 99: 'ो', 100: 'ौ',
    # Common ligatures and special chars
    162: 'ृ', 163: 'ज्ञ', 200: 'ष', 201: 'ख्', 205: 'छ', 215: 'य', 218: 'ध', 219: 'य', 220: 'ण', 222: 'थ',
    224: 'र', 229: 'त', 230: 'ध', 231: 'य', 232: 'म', 272: 'द', 282: 'त्र', 287: '्', 292: 'र',
    294: 'त्र', 302: 'ष', 419: 'र', 465: 'न', 467: 'न', 506: 'ड़', 509: 'क्ष', 547: 'ी', 568: 'क',
    574: 'य', 581: 'त', 585: 'क', 622: 'ध', 871: 'म', 872: 'व', 873: 'य', 874: 'व', 876: 'ध',
    # Additional common ones
    46: 'ष', 68: 'ं', 69: 'ः', 154: 'ी', 155: 'ु', 156: 'ू', 165: 'ै', 166: 'ो', 167: 'ौ',
    285: '्य', 286: '्र', 290: 'र्', 291: 'ल्', 293: 'व्', 295: '्म', 300: 'द्', 301: 'ध्',
}

BETTER_CORRECTIONS = {
    'अजुन(cid:91) (cid:874)वषाद योग': 'अर्जुन विषाद योग',
    'अजुन(cid:91)(cid:874)वषाद योग': 'अर्जुन विषाद योग',
    'धम(cid:162)(cid:91) े(cid:287)': 'धर्मक्षेत्र',
    'कु(cid:509)(cid:162)े(cid:287)': 'कुरुक्षेत्र',
    'मो(cid:162) सं(cid:219)यास योग': 'मोक्ष संन्यास योग',
    'रणनी(cid:467)त': 'रणनीति',
    'धतृरा(cid:231)(cid:282)': 'धृतराष्ट्र',
    'सां(cid:201)य योग': 'साख्य योग',
}

def fix_text_improved(text):
    """Fix Hindi text with better CID replacements."""
    if not text:
        return ""
    
    text = str(text)
    
    # Apply known corrections first
    for wrong, right in BETTER_CORRECTIONS.items():
        text = text.replace(wrong, right)
    
    # Replace remaining CID codes
    def replace_cid(m):
        cid = int(m.group(1))
        return BETTER_CID_MAP.get(cid, f"[cid:{cid}]")
    
    return re.sub(r'\(cid:(\d+)\)', replace_cid, text).strip()

# Load and fix Hindi data
with open('assets/json/shlok_data_hindi.json', 'r', encoding='utf-8') as f:
    hindi = json.load(f)

print('Fixing CID codes and encoding issues...\n')

cid_count_before = 0
cid_count_after = 0

for entry in hindi[1:]:  # Skip header
    for field in ['__2', '__4', '__6', '__7', '__8']:
        original = entry.get(field, '')
        cid_count_before += original.count('[cid:')
        
        fixed = fix_text_improved(original)
        entry[field] = fixed
        
        cid_count_after += fixed.count('[cid:')

# Save fixed data
with open('assets/json/shlok_data_hindi.json', 'w', encoding='utf-8') as f:
    json.dump(hindi, f, ensure_ascii=False, indent=2)

print(f'CID codes before: {cid_count_before}')
print(f'CID codes after: {cid_count_after}')
print(f'Codes fixed: {cid_count_before - cid_count_after}')
print(f'\n✅ Saved improved Hindi data')

# Show samples
print('\n=== SAMPLE ENTRIES AFTER FIX ===')
for idx in [1, 2, 50, 100]:
    if idx < len(hindi):
        entry = hindi[idx]
        print(f'\nEntry {idx}:')
        print(f'  Title: {entry["__2"]}')
        print(f'  Speaker: {entry["__7"]}')
        print(f'  Theme: {entry["__6"]}')
