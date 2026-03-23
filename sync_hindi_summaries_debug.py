#!/usr/bin/env python3
import json

# Load the English data with Hindi translations
with open('assets/json/shlok_data.json', 'r', encoding='utf-8') as f:
    english_data = json.load(f)

# Load the Hindi data
with open('assets/json/shlok_data_hindi.json', 'r', encoding='utf-8') as f:
    hindi_data = json.load(f)

# Build a map of (chapter, shlok_number) -> Hindi summary from English file
hindi_summaries_map = {}
for item in english_data[1:]:  # Skip header
    if '__1' in item and '__3' in item and '__8_hi' in item:
        key = (int(item['__1']) if isinstance(item['__1'], int) else item['__1'], 
               int(item['__3']) if isinstance(item['__3'], int) else item['__3'])
        hindi_summaries_map[key] = item['__8_hi']

print(f"Built map with {len(hindi_summaries_map)} entries")
print(f"Sample keys: {list(hindi_summaries_map.keys())[:5]}")

# Check what keys exist in hindi_data
sample_keys_hindi = []
for item in hindi_data[1:6]:
    key = (int(item.get('__1', 0)) if isinstance(item.get('__1'), int) else item.get('__1'), 
           int(item.get('__3', 0)) if isinstance(item.get('__3'), int) else item.get('__3'))
    sample_keys_hindi.append(key)

print(f"Sample Hindi data keys: {sample_keys_hindi}")

# Update Hindi data with these summaries
updated_count = 0
for item in hindi_data[1:]:  # Skip header
    if '__1' in item and '__3' in item:
        key = (int(item['__1']) if isinstance(item['__1'], int) else item['__1'], 
               int(item['__3']) if isinstance(item['__3'], int) else item['__3'])
        if key in hindi_summaries_map:
            item['__8'] = hindi_summaries_map[key]
            updated_count += 1

print(f"Updated {updated_count} Hindi summaries in shlok_data_hindi.json")

# Save the updated Hindi data
with open('assets/json/shlok_data_hindi.json', 'w', encoding='utf-8') as f:
    json.dump(hindi_data, f, ensure_ascii=False, indent=2)

print("✓ shlok_data_hindi.json saved successfully")
