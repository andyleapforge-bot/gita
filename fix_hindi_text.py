#!/usr/bin/env python3
import json
import sys

# Load the English data (which has _hi translations)
with open('assets/json/shlok_data.json', 'r', encoding='utf-8') as f:
    english_data = json.load(f)

# Load the Hindi data
with open('assets/json/shlok_data_hindi.json', 'r', encoding='utf-8') as f:
    hindi_data = json.load(f)

print("=" * 60)
print("FIXING HINDI JSON FILE - CONVERTING ENGLISH TO HINDI TEXT")
print("=" * 60)

# Build mapping of English text -> Hindi text from the English file
# We'll use the __2 (chapter), __4 (keywords), __6 (theme), __7 (speaker) fields

english_to_hindi = {
    "__2": {},  # Chapter names
    "__4": {},  # Keywords
    "__6": {},  # Themes
    "__7": {}   # Speakers
}

print("\n1. Building translation mappings from shlok_data.json...")
for shlok in english_data:
    # Map chapter names
    if "__2" in shlok and "__2_hi" in shlok:
        en_text = shlok["__2"].strip()
        hi_text = shlok["__2_hi"].strip()
        if en_text and hi_text:
            english_to_hindi["__2"][en_text] = hi_text
    
    # Map keywords
    if "__4" in shlok and "__4_hi" in shlok:
        en_text = shlok["__4"].strip()
        hi_text = shlok["__4_hi"].strip()
        if en_text and hi_text:
            english_to_hindi["__4"][en_text] = hi_text
    
    # Map themes
    if "__6" in shlok and "__6_hi" in shlok:
        en_text = shlok["__6"].strip()
        hi_text = shlok["__6_hi"].strip()
        if en_text and hi_text:
            english_to_hindi["__6"][en_text] = hi_text
    
    # Map speakers
    if "__7" in shlok and "__7_hi" in shlok:
        en_text = shlok["__7"].strip()
        hi_text = shlok["__7_hi"].strip()
        if en_text and hi_text:
            english_to_hindi["__7"][en_text] = hi_text

print(f"  ✓ Chapter translations: {len(english_to_hindi['__2'])}")
print(f"  ✓ Keywords translations: {len(english_to_hindi['__4'])}")
print(f"  ✓ Theme translations: {len(english_to_hindi['__6'])}")
print(f"  ✓ Speaker translations: {len(english_to_hindi['__7'])}")

# Sample translations
print("\n  Sample translations found:")
sample_count = 0
for field, mapping in english_to_hindi.items():
    if mapping and sample_count < 3:
        key = list(mapping.keys())[0]
        print(f"    {field}: '{key}' -> '{mapping[key]}'")
        sample_count += 1

# Now replace English text in Hindi file with Hindi equivalents
print("\n2. Converting English text to Hindi in shlok_data_hindi.json...")

updated_counts = {
    "__2": 0,
    "__4": 0,
    "__6": 0,
    "__7": 0
}

for shlok in hindi_data:
    # Convert chapter names
    if "__2" in shlok:
        current_text = shlok["__2"].strip()
        if current_text in english_to_hindi["__2"]:
            hindi_text = english_to_hindi["__2"][current_text]
            if current_text != hindi_text:  # Only count if it actually changed
                shlok["__2"] = hindi_text
                updated_counts["__2"] += 1
    
    # Convert keywords
    if "__4" in shlok:
        current_text = shlok["__4"].strip()
        if current_text in english_to_hindi["__4"]:
            hindi_text = english_to_hindi["__4"][current_text]
            if current_text != hindi_text:
                shlok["__4"] = hindi_text
                updated_counts["__4"] += 1
    
    # Convert themes
    if "__6" in shlok:
        current_text = shlok["__6"].strip()
        if current_text in english_to_hindi["__6"]:
            hindi_text = english_to_hindi["__6"][current_text]
            if current_text != hindi_text:
                shlok["__6"] = hindi_text
                updated_counts["__6"] += 1
    
    # Convert speakers
    if "__7" in shlok:
        current_text = shlok["__7"].strip()
        if current_text in english_to_hindi["__7"]:
            hindi_text = english_to_hindi["__7"][current_text]
            if current_text != hindi_text:
                shlok["__7"] = hindi_text
                updated_counts["__7"] += 1

print(f"\n  Converted:")
print(f"    ✓ Chapters (__2): {updated_counts['__2']} items")
print(f"    ✓ Keywords (__4): {updated_counts['__4']} items")
print(f"    ✓ Themes (__6): {updated_counts['__6']} items")
print(f"    ✓ Speakers (__7): {updated_counts['__7']} items")
print(f"    ✓ Total: {sum(updated_counts.values())} items converted to Hindi")

# Save the updated Hindi file
print("\n3. Saving updated Hindi JSON file...")
with open('assets/json/shlok_data_hindi.json', 'w', encoding='utf-8') as f:
    json.dump(hindi_data, f, ensure_ascii=False, indent=2)

print("\n" + "=" * 60)
print("✓ SUCCESS! Hindi JSON file updated with Hindi text")
print("=" * 60)
print("\nNext steps:")
print("  1. Run: flutter clean")
print("  2. Run: flutter run")
print("  3. Test Hindi mode to verify all text shows in Hindi")
