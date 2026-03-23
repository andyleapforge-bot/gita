#!/usr/bin/env python3
import json

# Load English data
with open('assets/json/shlok_data.json', 'r', encoding='utf-8') as f:
    english_data = json.load(f)

# Check shlok numbering for chapter 3
print("Chapter 3 shloks in English data:")
for i, item in enumerate(english_data):
    if item.get('__1') == 3:
        print(f"Index {i}: Chapter {item.get('__1')}, __3={item.get('__3')}, Title={item.get('__2', '')[:30]}")
        if i > 5:  # Show first few
            break
