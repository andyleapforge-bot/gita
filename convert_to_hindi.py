#!/usr/bin/env python3
import json

# Load English data with Hindi translations
with open('assets/json/shlok_data.json', 'r', encoding='utf-8') as f:
    english_data = json.load(f)

# Load Hindi data
with open('assets/json/shlok_data_hindi.json', 'r', encoding='utf-8', errors='replace') as f:
    hindi_data = json.load(f)

# Build translation maps from English data
title_translations = {}  # __2 -> __2_hi
speaker_translations = {}  # __7 -> __7_hi
theme_translations = {}  # __6 -> __6_hi
keywords_translations = {}  # __4 -> __4_hi
summary_translations = {}  # __8 -> __8_hi

for item in english_data[1:]:  # Skip header
    # Map English to Hindi for chapters/titles
    if '__2' in item and '__2_hi' in item:
        eng_title = item['__2']
        hi_title = item['__2_hi']
        if eng_title and hi_title:
            title_translations[eng_title] = hi_title
    
    # Map speakers
    if '__7' in item and '__7_hi' in item:
        eng_speaker = item['__7']
        hi_speaker = item['__7_hi']
        if eng_speaker and hi_speaker:
            speaker_translations[eng_speaker] = hi_speaker
    
    # Map themes
    if '__6' in item and '__6_hi' in item:
        eng_theme = item['__6']
        hi_theme = item['__6_hi']
        if eng_theme and hi_theme:
            theme_translations[eng_theme] = hi_theme
    
    # Map keywords
    if '__4' in item and '__4_hi' in item:
        eng_keywords = item['__4']
        hi_keywords = item['__4_hi']
        if eng_keywords and hi_keywords:
            keywords_translations[eng_keywords] = hi_keywords
    
    # Map summaries by index (they don't match by key)

print(f"Loaded translations:")
print(f"  Titles: {len(title_translations)}")
print(f"  Speakers: {len(speaker_translations)}")
print(f"  Themes: {len(theme_translations)}")
print(f"  Keywords: {len(keywords_translations)}")

# Now update Hindi data with translations
updated_titles = 0
updated_speakers = 0
updated_themes = 0
updated_keywords = 0
updated_summaries = 0

for i, item in enumerate(hindi_data):
    if i == 0:  # Skip header
        continue
    
    # Update titles (__2)
    if '__2' in item and item['__2'] in title_translations:
        old_title = item['__2']
        item['__2'] = title_translations[old_title]
        updated_titles += 1
    
    # Update speakers (__7)
    if '__7' in item and item['__7'] in speaker_translations:
        old_speaker = item['__7']
        item['__7'] = speaker_translations[old_speaker]
        updated_speakers += 1
    
    # Update themes (__6)
    if '__6' in item and item['__6'] in theme_translations:
        old_theme = item['__6']
        item['__6'] = theme_translations[old_theme]
        updated_themes += 1
    
    # Update keywords (__4)
    if '__4' in item and item['__4'] in keywords_translations:
        old_keywords = item['__4']
        item['__4'] = keywords_translations[old_keywords]
        updated_keywords += 1
    
    # Update summaries (__8) using index mapping
    if i < len(english_data) and '__8_hi' in english_data[i]:
        item['__8'] = english_data[i]['__8_hi']
        updated_summaries += 1

print(f"\nUpdated in Hindi file:")
print(f"  Titles: {updated_titles}")
print(f"  Speakers: {updated_speakers}")
print(f"  Themes: {updated_themes}")
print(f"  Keywords: {updated_keywords}")
print(f"  Summaries: {updated_summaries}")

# Save updated Hindi data
with open('assets/json/shlok_data_hindi.json', 'w', encoding='utf-8') as f:
    json.dump(hindi_data, f, ensure_ascii=False, indent=2)

print("\n✓ shlok_data_hindi.json updated successfully with Hindi text!")
