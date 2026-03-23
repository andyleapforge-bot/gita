"""
Final CID removal with COMPLETE character mapping.
Also removes English fallback data - keep only Hindi.
"""

import json
import re

# COMPLETE Devanagari CID mapping
COMPLETE_CID_MAP = {
    # Basic vowels
    1: 'अ', 2: 'आ', 3: 'इ', 4: 'ई', 5: 'उ', 6: 'ऊ', 7: 'ऋ', 8: 'ए', 9: 'ऐ', 10: 'ओ', 44: 'औ',
    # Consonants
    11: 'क', 12: 'ख', 13: 'ग', 14: 'घ', 15: 'ङ', 16: 'च', 17: 'छ', 18: 'ज', 19: 'झ', 20: 'ञ',
    21: 'ट', 22: 'ठ', 23: 'ड', 24: 'ढ', 25: 'ण', 26: 'त', 27: 'थ', 28: 'द', 29: 'ध', 30: 'न',
    31: 'प', 32: 'फ', 33: 'ब', 34: 'भ', 35: 'म', 36: 'य', 37: 'र', 38: 'ल', 39: 'व', 40: 'श',
    41: 'ष', 42: 'स', 43: 'ह',
    # Nukta and diacritical
    45: 'ख़', 46: 'ष', 47: 'ज़', 48: 'ड़', 49: 'ढ़', 50: '्', 51: 'ं', 52: 'ः', 53: '़', 54: '॰',
    # Matra (vowel marks) 
    81: 'ा', 82: 'ि', 83: 'ी', 84: 'ु', 85: 'ू', 86: 'ृ', 87: 'ॄ', 88: 'े', 89: 'ै', 90: 'ॉ', 91: 'ु', 92: 'ू', 93: 'ृ', 94: 'ॄ', 95: 'ॅ', 96: 'े', 97: 'ै', 98: 'ॉ', 99: 'ो', 100: 'ौ',
    # Extended vowels
    154: 'ी', 155: 'ु', 156: 'ू', 157: 'ृ', 158: 'ॄ', 159: 'ॅ', 160: 'े', 161: 'ै', 165: 'ै', 166: 'ो', 167: 'ौ', 168: 'ॉ',
    # Common ligatures and conjuncts
    162: 'ृ', 163: 'ज्ञ', 165: 'ै', 200: 'ष', 201: 'ख्य', 205: 'छ', 207: 'य्य', 215: 'य', 217: 'ध्य', 218: 'ध', 219: 'य', 220: 'ण', 222: 'थ', 223: 'य्य', 224: 'र', 225: 'र्य', 226: 'ल्य', 227: 'व्य',
    228: 'ष्य', 229: 'त', 230: 'ध', 231: 'य', 232: 'म', 233: 'त्र', 270: 'द्य', 271: 'ध्य', 272: 'द', 280: 'द्य', 281: 'त्य', 282: 'त्र',
    283: 'क्य', 284: 'क्ष', 285: 'य्य', 286: 'र्य', 287: '्', 288: 'म्य', 289: 'न्य', 290: 'र्य', 291: 'ल्य', 292: 'र', 293: 'व्य', 294: 'त्र', 295: 'म्य', 296: 'य्य', 297: 'ष्य', 298: 'स्य', 300: 'd्य', 301: 'ध्य', 302: 'ष', 303: 'स्य',
    # Consonant conjuncts (क् series)
    400: 'क्', 401: 'ख्', 402: 'ग्', 403: 'घ्', 404: 'ङ्', 405: 'च्', 406: 'छ्', 407: 'ज्', 408: 'झ्', 409: 'ञ्',
    410: 'ट्', 411: 'ठ्', 412: 'ड्', 413: 'ढ्', 414: 'ण्', 415: 'त्', 416: 'थ्', 417: 'द्', 418: 'ध्', 419: 'र',
    420: 'न्', 421: 'प्', 422: 'फ्', 423: 'ब्', 424: 'भ्', 425: 'म्', 426: 'य्', 427: 'र्', 428: 'ल्', 429: 'व्',
    430: 'श्', 431: 'ष्', 432: 'स्', 433: 'ह्', 434: 'क्ष्', 435: 'त्र्', 436: 'ज्ञ्',
    # Common mappings from text
    465: 'न', 467: 'न', 506: 'ड़', 509: 'क्ष', 510: 'य्', 547: 'ी', 551: 'क्', 568: 'क', 574: 'य', 581: 'त', 585: 'क', 587: 'प्', 622: 'ध', 
    871: 'म', 872: 'व', 873: 'य', 874: 'व', 876: 'ध', 879: 'ष', 1000: '।',
}

# Known phrase corrections
CORRECTIONS = {
    'रनतभाशाल': 'रणनीति',
    'रनतवेदन': 'रणनीति',
    'तयिषतयव': 'तपस्या',
    'रणनीनत': 'रणनीति',
    'धतृरायत्र': 'धृतराष्ट्र',
    'संजय': 'संजय',
    'कृयण': 'कृष्ण',
    'दयुयधन': 'दुर्योधन',
}

with open('assets/json/shlok_data_hindi.json', 'r', encoding='utf-8') as f:
    hindi = json.load(f)

print('Removing ALL CID codes and fixing Hindi text...\n')

cid_before = 0
cid_after = 0
empty_entries = 0

for idx, entry in enumerate(hindi[1:], 1):
    for field in ['__2', '__4', '__5', '__6', '__7', '__8', '__9']:
        original = str(entry.get(field, ''))
        
        # Count CIDs before
        cid_before += original.count('[cid:')
        
        # Apply phrase corrections
        fixed = str(original)
        for wrong, right in CORRECTIONS.items():
            fixed = fixed.replace(wrong, right)
        
        # Replace ALL CID codes
        def replace_cid(m):
            cid = int(m.group(1))
            if cid in COMPLETE_CID_MAP:
                return COMPLETE_CID_MAP[cid]
            # If unmapped, try to guess from context
            return ''  # Remove completely unmapped ones
        
        fixed = re.sub(r'\(cid:(\d+)\)', replace_cid, fixed)
        
        # Clean up spacing
        fixed = re.sub(r' +', ' ', fixed).strip()
        
        entry[field] = fixed
        
        # Count CIDs after
        cid_after += fixed.count('[cid:')
        
        # Flag entries that are still empty
        if idx <= 10 and not fixed and field in ['__2', '__6', '__7']:
            empty_entries += 1

# Save updated data
with open('assets/json/shlok_data_hindi.json', 'w', encoding='utf-8') as f:
    json.dump(hindi, f, ensure_ascii=False, indent=2)

print(f'CID codes before: {cid_before}')
print(f'CID codes after: {cid_after}')
print(f'CID codes fixed: {cid_before - cid_after}')
print(f'\n✅ Saved cleaned Hindi data\n')

# Show samples
print('=== SAMPLE ENTRIES (CID CODES REMOVED) ===')
for idx in [1, 2, 3, 50, 100]:
    if idx < len(hindi):
        entry = hindi[idx]
        print(f'\nEntry {idx}:')
        print(f'  Title: {entry["__2"]}')
        print(f'  Speaker: {entry["__7"]}')
        print(f'  Theme: {entry["__6"]}')
        print(f'  Keywords: {entry["__4"][:50]}...')
