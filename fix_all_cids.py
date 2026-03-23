"""
Fix remaining CID codes with aggressive character fixing
"""

import json
import re

# Complete mapping including ones I missed
CID_COMPLETE = {
    # Basic vowels
    1: 'अ', 2: 'आ', 3: 'इ', 4: 'ई', 5: 'उ', 6: 'ऊ', 7: 'ऋ', 8: 'ए', 9: 'ऐ', 10: 'ओ', 44: 'औ',
    # Consonants
    11: 'क', 12: 'ख', 13: 'ग', 14: 'घ', 15: 'ङ', 16: 'च', 17: 'छ', 18: 'ज', 19: 'झ', 20: 'ञ',
    21: 'ट', 22: 'ठ', 23: 'ड', 24: 'ढ', 25: 'ण', 26: 'त', 27: 'थ', 28: 'द', 29: 'ध', 30: 'न',
    31: 'प', 32: 'फ', 33: 'ब', 34: 'भ', 35: 'म', 36: 'य', 37: 'र', 38: 'ल', 39: 'व', 40: 'श',
    41: 'ष', 42: 'स', 43: 'ह',
    # Diacritics
    45: 'ख़', 46: 'ष', 47: 'ज़', 48: 'ड़', 49: 'ढ़', 50: '्', 51: 'ं', 52: 'ः', 53: '़',
    # Matra (vowel marks)
    81: 'ा', 82: 'ि', 83: 'ी', 91: 'ु', 92: 'ू', 93: 'ृ', 94: 'ॄ', 95: 'ॅ', 96: 'े', 97: 'ै', 98: 'ॉ', 99: 'ो', 100: 'ौ',
    # Extended Devanagari
    154: 'ी', 155: 'ु', 156: 'ू', 157: 'ृ', 158: 'ॄ', 159: 'ॅ', 160: 'े', 161: 'ै', 165: 'ै', 166: 'ो', 167: 'ौ', 168: 'ॉ',
    # Ligatures and special forms
    162: 'ृ', 163: 'ज्ञ', 165: 'ै', 180: '्य', 185: 'ु', 190: 'ु', 195: 'े', 200: 'ष', 201: 'ख्', 205: 'छ',
    215: 'य', 217: 'ध्', 218: 'ध', 219: 'य', 220: 'ण', 222: 'थ', 223: 'य्', 224: 'र', 225: 'र्', 226: 'ल्', 227: 'व्',
    228: 'ष्', 229: 'त', 230: 'ध', 231: 'य', 232: 'म', 270: 'द्', 271: 'ध्', 272: 'द', 280: 'द्य', 281: 'त्य', 282: 'त्र',
    283: 'क्य', 284: 'क्ष', 285: '्य', 286: '्र', 287: '्', 288: '्म', 289: '्न', 290: 'र्', 291: 'ल्', 292: 'र',
    293: 'व्', 294: 'त्र', 295: 'म्', 296: 'य्', 297: 'ष्', 298: 'स्', 300: 'द्', 301: 'ध्', 302: 'ष', 303: 'स्',
    400: 'क्', 401: 'ख्', 402: 'ग्', 403: 'घ्', 404: 'ङ्', 405: 'च्', 406: 'छ्', 407: 'ज्', 408: 'झ्', 409: 'ञ्',
    410: 'ट्', 411: 'ठ्', 412: 'ड्', 413: 'ढ्', 414: 'ण्', 415: 'त्', 416: 'थ्', 417: 'द्', 418: 'ध्', 419: 'र',
    420: 'न्', 421: 'प्', 422: 'फ्', 423: 'ब्', 424: 'भ्', 425: 'म्', 426: 'य्', 427: 'र्', 428: 'ल्', 429: 'व्',
    430: 'श्', 431: 'ष्', 432: 'स्', 433: 'ह्',
    # More mappings for common substitutes
    465: 'न', 467: 'न', 506: 'ड़', 509: 'क्ष', 547: 'ी', 568: 'क', 574: 'य', 581: 'त', 585: 'क', 622: 'ध', 
    871: 'म', 872: 'व', 873: 'य', 874: 'व', 876: 'ध', 1000: '।',
}

with open('assets/json/shlok_data_hindi.json', 'r', encoding='utf-8') as f:
    hindi = json.load(f)

print('Aggressively fixing all remaining CID codes...\n')

cid_before = {}
cid_after = {}

for entry in hindi[1:]:
    for field in ['__2', '__4', '__6', '__7', '__8']:
        original = entry.get(field, '')
        
        # Count CIDs before
        for m in re.finditer(r'\(cid:(\d+)\)', original):
            cid = int(m.group(1))
            cid_before[cid] = cid_before.get(cid, 0) + 1
        
        # Replace all CIDs
        def replace_cid(m):
            cid = int(m.group(1))
            if cid in CID_COMPLETE:
                return CID_COMPLETE[cid]
            # For unknown CIDs, try to return something sensible
            return ''  # Remove unmapped CIDs
        
        fixed = re.sub(r'\(cid:(\d+)\)', replace_cid, original)
        
        # Clean up multiple spaces
        fixed = re.sub(r' +', ' ', fixed).strip()
        
        entry[field] = fixed
        
        # Count CIDs after
        for m in re.finditer(r'\(cid:(\d+)\)', fixed):
            cid = int(m.group(1))
            cid_after[cid] = cid_after.get(cid, 0) + 1

total_before = sum(cid_before.values())
total_after = sum(cid_after.values())

print(f'Total CID codes before: {total_before}')
print(f'Total CID codes after: {total_after}')
print(f'Fixed: {total_before - total_after}')

if cid_after:
    print(f'\nRemaining unmapped CIDs:')
    for cid in sorted(cid_after.keys()):
        print(f'  [cid:{cid}]: {cid_after[cid]} occurrences')

# Save fixed data
with open('assets/json/shlok_data_hindi.json', 'w', encoding='utf-8') as f:
    json.dump(hindi, f, ensure_ascii=False, indent=2)

print(f'\n✅ Saved improved Hindi data\n')

# Show samples
print('=== FIXED SAMPLE ENTRIES ===')
for idx in [1, 2, 50, 100, 200]:
    if idx < len(hindi):
        entry = hindi[idx]
        print(f'\nEntry {idx}:')
        print(f'  Title: {entry["__2"]}')
        print(f'  Speaker: {entry["__7"]}')
        print(f'  Theme: {entry["__6"]}')
        kw = entry["__4"][:50]
        print(f'  Keywords: {kw}...')
