#!/usr/bin/env python3
import json

# Load English data
with open('assets/json/shlok_data.json', 'r', encoding='utf-8') as f:
    english_data = json.load(f)

# Check Chapter 3 shloks in English
print("First 5 Chapter 3 shloks in English data:")
count = 0
for i, item in enumerate(english_data):
    if item.get('__1') == 3:
        print(f"Index {i}: Chapter {item.get('__1')}, __3={item.get('__3')}, __8_hi={bool(item.get('__8_hi'))}")
        count += 1
        if count >= 5:
            break
