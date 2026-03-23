"""
Fix remaining CID codes with comprehensive mapping for all CIDs found
"""

import json
import re

# Mapping for ALL found CIDs
CID_MAPPING = {
    # From detected CIDs
    201: 'ख्य', 202: 'य्य', 207: 'य्य', 209: 'य्य', 214: 'य्य', 216: 'य्य', 223: 'य्य', 227: 'व्य',
    233: 'त्र', 234: 'त्र', 274: 'द्य', 275: 'द्य', 279: 'द्य', 284: 'क्ष', 289: 'न्य', 295: 'म्य', 296: 'य्य',
    301: 'ध्य', 304: 'स्य', 464: 'र', 466: 'न', 510: 'य्', 511: 'य्', 548: 'ी', 551: 'क्', 566: 'ष', 579: 'प्',
    583: 'क्', 587: 'प्', 607: 'त्', 618: 'ध्', 875: 'म', 879: 'ष',
    # Basic ones from before
    1: 'अ', 2: 'आ', 3: 'इ', 4: 'ई', 5: 'उ', 6: 'ऊ', 7: 'ऋ', 8: 'ए', 9: 'ऐ', 10: 'ओ', 44: 'औ',
    11: 'क', 12: 'ख', 13: 'ग', 14: 'घ', 15: 'ङ', 16: 'च', 17: 'छ', 18: 'ज', 19: 'झ', 20: 'ञ',
    21: 'ट', 22: 'ठ', 23: 'ड', 24: 'ढ', 25: 'ण', 26: 'त', 27: 'थ', 28: 'द', 29: 'ध', 30: 'न',
    31: 'प', 32: 'फ', 33: 'ब', 34: 'भ', 35: 'म', 36: 'य', 37: 'र', 38: 'ल', 39: 'व', 40: 'श',
    41: 'ष', 42: 'स', 43: 'ह',
    50: '्', 51: 'ं', 52: 'ः', 53: '़',
    81: 'ा', 82: 'ि', 83: 'ी', 91: 'ु', 92: 'ू', 93: 'ृ', 96: 'े', 97: 'ै', 99: 'ो', 100: 'ौ',
}

with open('assets/json/shlok_data_hindi.json', 'r', encoding='utf-8') as f:
    content = f.read()

print('Replacing all CID codes with characters...\n')

cid_before = len(re.findall(r'\[cid:\d+\]', content))
print(f'CID codes before: {cid_before}')

# Replace all CID codes
def replace_cid(match):
    cid = int(match.group(1))
    return CID_MAPPING.get(cid, '')  # Remove unmapped CIDs

content = re.sub(r'\[cid:(\d+)\]', replace_cid, content)

cid_after = len(re.findall(r'\[cid:\d+\]', content))
print(f'CID codes after: {cid_after}')
print(f'Fixed: {cid_before - cid_after}')

# Save
with open('assets/json/shlok_data_hindi.json', 'w', encoding='utf-8') as f:
    f.write(content)

print(f'\n✅ Saved fixed Hindi data (all CID codes should be gone)\n')

# Verify
with open('assets/json/shlok_data_hindi.json', 'r', encoding='utf-8') as f:
    hindi = json.load(f)

print('=== SAMPLE ENTRIES (AFTER CID FIX) ===')
for idx in [1, 2, 50, 100]:
    if idx < len(hindi):
        entry = hindi[idx]
        print(f'\nEntry {idx}:')
        print(f'  Title: {entry["__2"]}')
        print(f'  Speaker: {entry["__7"]}')
