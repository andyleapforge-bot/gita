#!/usr/bin/env python3
import json

# Load Hindi data
with open('assets/json/shlok_data_hindi.json', 'r', encoding='utf-8') as f:
    hindi_data = json.load(f)

# Find where chapter 3 starts
for i, item in enumerate(hindi_data):
    if item.get('__1') == 3 and item.get('__3') == 1:
        print(f"Chapter 3 Shlok 1 found at index {i}")
        print(f"Item: {item}")
        break
    if item.get('__1') == 3:
        print(f"Chapter 3 item at index {i}: Shlok {item.get('__3')}")
        if i > 300:
            break

# Count total shloks
print(f"\nTotal items in Hindi data: {len(hindi_data)}")
