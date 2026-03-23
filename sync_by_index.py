#!/usr/bin/env python3
import json

# Load the English data with Hindi translations
with open('assets/json/shlok_data.json', 'r', encoding='utf-8') as f:
    english_data = json.load(f)

# Load the Hindi data
with open('assets/json/shlok_data_hindi.json', 'r', encoding='utf-8', errors='replace') as f:
    hindi_data = json.load(f)

# Since both files have the same structure and indices correspond to the same shlok,
# we can simply copy __8_hi to __8 using indices
updated_count = 0
for i in range(1, len(english_data)):  # Skip header at index 0
    if '__8_hi' in english_data[i] and i < len(hindi_data):
        hindi_data[i]['__8'] = english_data[i]['__8_hi']
        updated_count += 1

print(f"Updated {updated_count} Hindi summaries using index mapping")

# Save the updated Hindi data
with open('assets/json/shlok_data_hindi.json', 'w', encoding='utf-8') as f:
    json.dump(hindi_data, f, ensure_ascii=False, indent=2)

print("✓ shlok_data_hindi.json saved successfully")
