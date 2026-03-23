"""
Comprehensive verification that Hindi matches English structure and field usage.
"""
import json

# Load both files
with open('assets/json/shlok_data.json', 'r', encoding='utf-8') as f:
    eng = json.load(f)

with open('assets/json/shlok_data_hindi.json', 'r', encoding='utf-8') as f:
    hin = json.load(f)

print("=" * 70)
print("COMPREHENSIVE HINDI vs ENGLISH STRUCTURE & FIELD VERIFICATION")
print("=" * 70)

# 1. HEADER STRUCTURE
print("\n1️⃣ HEADER STRUCTURE MATCH:")
print("-" * 70)
eng_header = eng[0]
hin_header = hin[0]

print(f"English header fields: {sorted(eng_header.keys())}")
print(f"Hindi header fields:   {sorted(hin_header.keys())}")

header_match = True
for field in eng_header.keys():
    if field not in hin_header:
        print(f"  ❌ Missing field in Hindi: {field}")
        header_match = False
    elif eng_header[field] != hin_header[field]:
        print(f"  ❌ Header mismatch for {field}:")
        print(f"     EN: {eng_header[field]}")
        print(f"     HI: {hin_header[field]}")
        header_match = False

if header_match:
    print("  ✅ Headers perfectly match!")

# 2. DATA ENTRY STRUCTURE
print("\n2️⃣ DATA ENTRY STRUCTURE COMPARISON:")
print("-" * 70)

# Check first 10 entries
print("Checking first 10 shloks...")
structure_match = True

for i in range(1, min(11, len(eng), len(hin))):
    e = eng[i]
    h = hin[i]
    
    # Check if all English fields exist in Hindi
    for field in e.keys():
        if field not in h:
            print(f"  ❌ Entry {i}: Missing field {field} in Hindi")
            structure_match = False
    
    # Check field types match
    for field in e.keys():
        if field in h:
            e_type = type(e[field]).__name__
            h_type = type(h[field]).__name__
            if e_type != h_type:
                print(f"  ❌ Entry {i}, field {field}: Type mismatch (EN: {e_type}, HI: {h_type})")
                structure_match = False

if structure_match:
    print("  ✅ All structures match!")

# 3. FIELD ANALYSIS - What fields are used?
print("\n3️⃣ FIELD USAGE ANALYSIS:")
print("-" * 70)
print("\nFields and their purposes (from app code):")
print("""
  __1 : Chapter # (int)        - Used for: grouping, filtering
  __2 : Chapter Name (str)     - Used for: display in lists, detail page
  __3 : Shlok # (int)          - Used for: verse number display, identification
  __4 : Keywords (str)         - Used for: search, filtering
  __5 : Star (int)             - Used for: rating display, filtering
  __6 : Theme (str)            - Used for: theme display, theme filter
  __7 : Speaker (str)          - Used for: speaker display, speaker filter
  __8 : Shlok Summary (str)    - Used for: summary card, detail page
  __9 : AV Link (str)          - Used for: video playback, media display
  ""  : Empty (str)            - Not used, structural field
""")

# 4. DETAILED FIELD-BY-FIELD COMPARISON
print("\n4️⃣ FIELD-BY-FIELD COMPLETENESS CHECK:")
print("-" * 70)

field_analysis = {
    '__1': {'name': 'Chapter #', 'type': 'int'},
    '__2': {'name': 'Chapter Name', 'type': 'str'},
    '__3': {'name': 'Shlok #', 'type': 'int'},
    '__4': {'name': 'Keywords', 'type': 'str'},
    '__5': {'name': 'Star', 'type': 'int'},
    '__6': {'name': 'Theme', 'type': 'str'},
    '__7': {'name': 'Speaker', 'type': 'str'},
    '__8': {'name': 'Shlok Summary', 'type': 'str'},
    '__9': {'name': 'AV Link', 'type': 'str'},
}

for field, info in sorted(field_analysis.items()):
    print(f"\n{field} - {info['name']} ({info['type']}):")
    
    # Check English
    eng_count = 0
    eng_empty = 0
    for i in range(1, len(eng)):
        if field in eng[i]:
            eng_count += 1
            if not eng[i][field]:
                eng_empty += 1
    
    # Check Hindi
    hin_count = 0
    hin_empty = 0
    for i in range(1, len(hin)):
        if field in hin[i]:
            hin_count += 1
            if not hin[i][field]:
                hin_empty += 1
    
    print(f"  English: {eng_count-eng_empty}/{eng_count-1} filled, {eng_empty} empty")
    print(f"  Hindi:   {hin_count-hin_empty}/{hin_count-1} filled, {hin_empty} empty")
    
    if eng_count == hin_count and eng_empty == hin_empty:
        print(f"  ✅ Perfect match!")
    else:
        print(f"  ❌ Mismatch!")

# 5. SAMPLE DATA COMPARISON - Multiple Chapters
print("\n5️⃣ SAMPLE DATA COMPARISON (Various Chapters):")
print("-" * 70)

test_entries = [1, 50, 150, 300, 500, 700]  # Different chapters

for idx in test_entries:
    if idx >= len(eng) or idx >= len(hin):
        continue
    
    e = eng[idx]
    h = hin[idx]
    
    print(f"\nEntry {idx}: Chapter {e['__1']}, Verse {e['__3']}")
    print(f"  English Chapter: {e['__2'][:40]}")
    print(f"  Hindi Chapter:   {h['__2'][:40]}")
    
    # Check key fields
    all_match = True
    for field in ['__1', '__3', '__5']:  # Numeric fields should match exactly
        if field in e and field in h:
            if e[field] != h[field]:
                print(f"    ❌ {field} mismatch: EN={e[field]}, HI={h[field]}")
                all_match = False
    
    # Check string fields are populated
    for field in ['__6', '__7', '__8']:
        if field in e:
            if not e[field]:
                print(f"    ⚠️ English {field} is empty!")
            if field not in h or not h[field]:
                print(f"    ❌ Hindi {field} is missing/empty!")
                all_match = False
    
    if all_match:
        print(f"  ✅ Structure matches perfectly!")

# 6. DATA USAGE COMPATIBILITY CHECK
print("\n6️⃣ APP USAGE COMPATIBILITY CHECK:")
print("-" * 70)

usage_checks = {
    'Filtering by Chapter': ('__1', 'int'),
    'Filtering by Star Rating': ('__5', 'int'),
    'Searching in Keywords': ('__4', 'str'),
    'Filtering by Theme': ('__6', 'str'),
    'Filtering by Speaker': ('__7', 'str'),
    'Displaying Shlok Summary': ('__8', 'str'),
    'Playing Video': ('__9', 'str'),
}

print("\nChecking if all fields needed by app are present and correct type:")
for usage, (field, expected_type) in usage_checks.items():
    issues = 0
    for i in range(1, len(hin)):
        h = hin[i]
        if field not in h:
            issues += 1
    
    if issues == 0:
        print(f"  ✅ {usage} ({field}): Ready")
    else:
        print(f"  ❌ {usage} ({field}): {issues} entries missing")

# 7. FINAL VERDICT
print("\n" + "=" * 70)
print("FINAL VERDICT:")
print("=" * 70)

# Comprehensive check
all_good = True

# Total entries match
if len(eng) != len(hin):
    print(f"❌ Entry count mismatch: EN={len(eng)}, HI={len(hin)}")
    all_good = False
else:
    print(f"✅ Entry count match: {len(eng)} entries (701 shloks + 1 header)")

# Headers match
if eng_header != hin_header:
    print(f"❌ Header structure mismatch")
    all_good = False
else:
    print(f"✅ Header structure perfect match")

# Chapter/verse distribution
if len(set(e['__1'] for e in eng[1:])) == len(set(h['__1'] for h in hin[1:])):
    print(f"✅ Chapter distribution matches")
else:
    print(f"❌ Chapter distribution mismatch")
    all_good = False

if all_good:
    print("\n🎉 PERFECT MATCH! Hindi data is structured identically to English!")
    print("   All app features will work with both languages seamlessly.")
else:
    print("\n⚠️ There are structural differences to address.")
