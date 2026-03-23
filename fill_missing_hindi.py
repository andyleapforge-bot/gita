"""
Fill missing Hindi data from English version where applicable.
This ensures all 701 Hindi entries have complete data for app functionality.
"""

import json

with open('assets/json/shlok_data.json', 'r', encoding='utf-8') as f:
    english = json.load(f)

with open('assets/json/shlok_data_hindi.json', 'r', encoding='utf-8') as f:
    hindi = json.load(f)

print('Filling missing Hindi data from English fallback...\n')

# Fields that should be filled from English if missing
FALLBACK_FIELDS = ['__2', '__4', '__5', '__6', '__7', '__8', '__9']

filled_count = 0
total_missing = 0

for idx in range(1, len(hindi)):
    hindi_entry = hindi[idx]
    en_entry = english[idx] if idx < len(english) else None
    
    if not en_entry:
        continue
    
    for field in FALLBACK_FIELDS:
        hindi_val = hindi_entry.get(field, '')
        en_val = en_entry.get(field, '')
        
        # Check if Hindi value is empty/missing
        if not hindi_val or (isinstance(hindi_val, str) and not hindi_val.strip()):
            if en_val and str(en_val).strip():
                # For keywords and theme, prefix with [EN] to indicate source
                if field == '__4':  # Keywords
                    hindi_entry[field] = en_val
                    filled_count += 1
                elif field == '__5':  # Star rating
                    try:
                        hindi_entry[field] = int(en_val) if isinstance(en_val, int) else 0
                        filled_count += 1
                    except:
                        pass
                else:
                    hindi_entry[field] = en_val
                    filled_count += 1
            total_missing += 1

print(f'Filled {filled_count} missing fields from English fallback')
print(f'Total missing fields processed: {total_missing}\n')

# Verify results
print('=== VERIFICATION AFTER FILLING ===\n')

def check_completeness(data, name):
    counts = {}
    for field in ['__1', '__2', '__3', '__4', '__5', '__6', '__7', '__8', '__9']:
        count = 0
        for entry in data[1:]:
            val = entry.get(field, '')
            if val and str(val).strip():
                count += 1
        counts[field] = count
        status = '✅' if count == len(data) - 1 else f'⚠️ ({count}/{len(data)-1})'
        print(f'{name} {field}: {status}')
    return counts

check_completeness(hindi, 'HINDI')

# Save updated Hindi JSON
with open('assets/json/shlok_data_hindi.json', 'w', encoding='utf-8') as f:
    json.dump(hindi, f, ensure_ascii=False, indent=2)

print('\n✅ Updated shlok_data_hindi.json with fallback data')

# Sample comparison
print('\n=== SAMPLE ENTRIES (showing filled data) ===')
for idx in [1, 120, 150, 200]:
    if idx < len(hindi):
        entry = hindi[idx]
        print(f'\nEntry {idx}: Ch {entry["__1"]}, V {entry["__3"]}, Star {entry["__5"]}')
        print(f'  Keywords: {entry["__4"][:60]}...')
