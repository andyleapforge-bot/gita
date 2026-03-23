#!/usr/bin/env python3
import json

# Load the English data
with open('assets/json/shlok_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Count __8_hi fields
count = 0
for item in data[1:]:  # Skip header
    if '__8_hi' in item:
        count += 1
        if count <= 10:
            print(f"Shlok {item.get('__1')}.{item.get('__3')}: {item.get('__8_hi', '')[:50]}...")

print(f"\nTotal shloks with __8_hi: {count}")
