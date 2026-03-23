#!/usr/bin/env python3
import json

# Load the English data with Hindi translations
with open('assets/json/shlok_data.json', 'r', encoding='utf-8') as f:
    english_data = json.load(f)

# Get chapters that have __8_hi
chapters_with_hindi = set()
for item in english_data[1:]:
    if '__8_hi' in item:
        chapters_with_hindi.add(item.get('__1'))

print(f"Chapters with __8_hi: {sorted(chapters_with_hindi)}")

# Build a map of (chapter, shlok_number) -> Hindi summary from English file
hindi_summaries_map = {}
for item in english_data[1:]:  # Skip header
    if '__1' in item and '__3' in item and '__8_hi' in item:
        key = (item['__1'], item['__3'])
        hindi_summaries_map[key] = item['__8_hi']

# Load the Hindi data
with open('assets/json/shlok_data_hindi.json', 'r', encoding='utf-8') as f:
    hindi_data = json.load(f)

# Update Hindi data with these summaries
updated_count = 0
for item in hindi_data[1:]:  # Skip header
    if '__1' in item and '__3' in item:
        key = (item['__1'], item['__3'])
        if key in hindi_summaries_map:
            item['__8'] = hindi_summaries_map[key]
            updated_count += 1

print(f"Updated {updated_count} Hindi summaries in shlok_data_hindi.json")

# Save the updated Hindi data with nice formatting
with open('assets/json/shlok_data_hindi.json', 'w', encoding='utf-8') as f:
    json.dump(hindi_data, f, ensure_ascii=False, indent=2)

print("✓ shlok_data_hindi.json saved successfully")
