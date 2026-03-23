#!/usr/bin/env python3
import json

with open('assets/json/shlok_data_hindi.json', 'r', encoding='utf-8', errors='replace') as f:
    h = json.load(f)
    
print(f"Index 120: Chapter {h[120].get('__1')}, Shlok {h[120].get('__3')}, Title: {h[120].get('__2', '')[:30]}")
