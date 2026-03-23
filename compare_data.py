"""
Compare English and Hindi JSON files to verify complete data extraction.
"""
import json

# Load both files
with open('assets/json/shlok_data.json', 'r', encoding='utf-8') as f:
    eng = json.load(f)

with open('assets/json/shlok_data_hindi.json', 'r', encoding='utf-8') as f:
    hin = json.load(f)

print("=" * 60)
print("DETAILED COMPARISON: ENGLISH vs HINDI")
print("=" * 60)

print(f"\n📊 TOTAL ENTRIES:")
print(f"  English: {len(eng)} total (1 header + {len(eng)-1} shloks)")
print(f"  Hindi:   {len(hin)} total (1 header + {len(hin)-1} shloks)")
print(f"  Missing from Hindi: {len(eng) - len(hin)} shloks")

# Check structure match
print(f"\n🔧 STRUCTURE MATCH:")
eng_header = eng[0]
hin_header = hin[0]
match = eng_header == hin_header
print(f"  Headers match: {match}")
if not match:
    print(f"    English: {eng_header}")
    print(f"    Hindi:   {hin_header}")

# Check English coverage
print(f"\n📚 ENGLISH COVERAGE:")
eng_chapters = {}
for i in range(1, len(eng)):
    ch = eng[i]['__1']
    if ch not in eng_chapters:
        eng_chapters[ch] = 0
    eng_chapters[ch] += 1

print(f"  Total chapters: {len(eng_chapters)}")
print(f"  Chapters: {min(eng_chapters.keys())} to {max(eng_chapters.keys())}")

# Show distribution
chapter_list = sorted(eng_chapters.items())
print(f"\n  Chapter breakdown (first 5):")
for ch, count in chapter_list[:5]:
    print(f"    Chapter {ch}: {count:3d} verses")

print(f"  ... (middle chapters omitted)")

print(f"\n  Chapter breakdown (last 5):")
for ch, count in chapter_list[-5:]:
    print(f"    Chapter {ch}: {count:3d} verses")

# Check Hindi coverage
print(f"\n📚 HINDI COVERAGE:")
hin_chapters = {}
for i in range(1, len(hin)):
    ch = hin[i]['__1']
    if ch not in hin_chapters:
        hin_chapters[ch] = 0
    hin_chapters[ch] += 1

print(f"  Total chapters: {len(hin_chapters)}")
print(f"  Chapters: {min(hin_chapters.keys())} to {max(hin_chapters.keys())}")

# Show distribution
chapter_list = sorted(hin_chapters.items())
print(f"\n  Chapter breakdown (first 5):")
for ch, count in chapter_list[:5]:
    print(f"    Chapter {ch}: {count:3d} verses")

print(f"  ... (middle chapters omitted)")

print(f"\n  Chapter breakdown (last 5):")
for ch, count in chapter_list[-5:]:
    print(f"    Chapter {ch}: {count:3d} verses")

# Compare chapters
print(f"\n✅ CHAPTER MATCHING:")
all_chapters = set(eng_chapters.keys()) | set(hin_chapters.keys())
missing = sorted(set(eng_chapters.keys()) - set(hin_chapters.keys()))
extra = sorted(set(hin_chapters.keys()) - set(eng_chapters.keys()))

if missing:
    print(f"  ❌ Chapters in English but NOT in Hindi: {missing}")
if extra:
    print(f"  ❌ Chapters in Hindi but NOT in English: {extra}")

if not missing and not extra:
    print(f"  ✅ All {len(all_chapters)} chapters present in both!")

# Per-chapter comparison
print(f"\n📊 VERSES PER CHAPTER:")
mismatches = []
for ch in sorted(all_chapters):
    eng_count = eng_chapters.get(ch, 0)
    hin_count = hin_chapters.get(ch, 0)
    if eng_count != hin_count:
        mismatches.append((ch, eng_count, hin_count))

if mismatches:
    print(f"  ❌ Chapters with different verse counts:")
    for ch, eng_cnt, hin_cnt in mismatches[:10]:
        print(f"    Chapter {ch}: English={eng_cnt}, Hindi={hin_cnt}, Diff={eng_cnt-hin_cnt}")
    if len(mismatches) > 10:
        print(f"    ... and {len(mismatches)-10} more")
else:
    print(f"  ✅ All chapters have matching verse counts!")

# Sample data comparison
print(f"\n📝 SAMPLE DATA COMPARISON:")
print(f"\n  Chapter 1, Verse 1:")
e1 = eng[1] if len(eng) > 1 else {}
h1 = hin[1] if len(hin) > 1 else {}

for key in ['__1', '__2', '__3', '__6', '__7', '__8']:
    e_val = e1.get(key, '(missing)')
    h_val = h1.get(key, '(missing)')
    match = "✅" if (e_val and h_val and e_val != h_val) else ("✅" if e_val == h_val else "❌")
    print(f"    {key}: {match}")
    if e_val != h_val:
        print(f"      EN: {str(e_val)[:50]}")
        print(f"      HI: {str(h_val)[:50]}")

print("\n" + "=" * 60)
