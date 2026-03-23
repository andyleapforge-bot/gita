#!/usr/bin/env python3
import json

# Load both files
with open('assets/json/shlok_data.json', 'r', encoding='utf-8') as f:
    english_data = json.load(f)

with open('assets/json/shlok_data_hindi.json', 'r', encoding='utf-8') as f:
    hindi_data = json.load(f)

# Check first item with __8_hi from English
for item in english_data[1:]:
    if '__8_hi' in item:
        print(f"English sample: Chapter type={type(item['__1'])}, value={item['__1']}")
        print(f"English sample: Shlok type={type(item['__3'])}, value={item['__3']}")
        print(f"English key: ({item['__1']}, {item['__3']})")
        break

# Check first item from Hindi
for item in hindi_data[1:]:
    if item.get('__1') and item.get('__3'):
        print(f"\nHindi sample: Chapter type={type(item['__1'])}, value={item['__1']}")
        print(f"Hindi sample: Shlok type={type(item['__3'])}, value={item['__3']}")
        print(f"Hindi key: ({item['__1']}, {item['__3']})")
        break

# Now let's find a matching key manually
print("\nLooking for chapter 3 shlok 1...")
for item in english_data[1:]:
    if item.get('__1') == 3 and item.get('__3') == 1:
        print(f"Found in English: {item.get('__8_hi', 'NO FIELD')[:50]}")

for item in hindi_data[1:]:
    if item.get('__1') == 3 and item.get('__3') == 1:
        print(f"Found in Hindi: {item.get('__8', 'NO FIELD')[:50]}")
