"""Verify the Hindi JSON is correctly formatted."""
import json

with open('assets/json/shlok_data_hindi.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"✅ JSON is valid!")
print(f"📊 Total entries: {len(data)} (header + {len(data)-1} shloks)")

print("\n📌 First 5 entries:")
for i in range(1, min(6, len(data))):
    entry = data[i]
    print(f"\n  Entry {i}: Chapter {entry['__1']}, Verse {entry['__3']}")
    print(f"    Title:   {entry['__2'][:50]}")
    print(f"    Theme:   {entry['__6'][:40]}")
    print(f"    Speaker: {entry['__7'][:40]}")
    print(f"    Summary: {entry['__8'][:60]}")

# Check for remaining CID codes
cid_count = 0
for entry in data[1:]:
    for field in ['__2', '__6', '__7', '__8']:
        cid_count += entry[field].count('(cid:')

print(f"\n📈 CID codes remaining in data: {cid_count}")

# Compare with English
with open('assets/json/shlok_data.json', 'r', encoding='utf-8') as f:
    eng_data = json.load(f)

print(f"\n📊 Comparison:")
print(f"  English entries: {len(eng_data)-1}")
print(f"  Hindi entries:   {len(data)-1}")
