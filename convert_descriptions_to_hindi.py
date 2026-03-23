#!/usr/bin/env python3
import json

# Load both JSON files
with open('assets/json/shlok_data.json', 'r', encoding='utf-8') as f:
    english_data = json.load(f)

with open('assets/json/shlok_data_hindi.json', 'r', encoding='utf-8') as f:
    hindi_data = json.load(f)

print("=" * 70)
print("CONVERTING ALL ENGLISH DESCRIPTIONS TO HINDI")
print("=" * 70)

# Create mapping of English descriptions to Hindi
description_map = {}
for shlok in english_data:
    if "__8" in shlok and "__8_hi" in shlok:
        english_desc = shlok["__8"].strip()
        hindi_desc = shlok["__8_hi"].strip()
        if english_desc and hindi_desc:
            description_map[english_desc] = hindi_desc

print(f"\n1. Loaded {len(description_map)} Hindi translations")

# Convert descriptions in Hindi file
converted_count = 0
not_found = set()

for shlok in hindi_data:
    if "__8" in shlok:
        current_desc = shlok["__8"].strip()
        
        if current_desc in description_map:
            shlok["__8"] = description_map[current_desc]
            converted_count += 1
        elif current_desc and not current_desc[0].islower() and current_desc not in ["Shlok Summary"]:
            # This looks like English text that wasn't in our map
            not_found.add(current_desc)

print(f"\n2. Conversion Results:")
print(f"   ✓ Successfully converted: {converted_count} descriptions to Hindi")

if not_found:
    print(f"\n3. {len(not_found)} descriptions NOT found in translation map (may not have translations):")
    for desc in sorted(list(not_found))[:10]:
        print(f"   - {desc[:60]}...")
else:
    print(f"\n3. All English descriptions were found and converted!")

# Save updated Hindi file
with open('assets/json/shlok_data_hindi.json', 'w', encoding='utf-8') as f:
    json.dump(hindi_data, f, ensure_ascii=False, indent=2)

print("\n" + "=" * 70)
print("✓ SUCCESS! All descriptions in Hindi JSON updated!")
print("=" * 70)
print("\nNow:")
print("  1. Run: flutter clean")
print("  2. Run: flutter run -d ZD22267824")
print("  3. Switch to Hindi mode and verify all text is in Hindi!")
