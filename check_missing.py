import json

with open('assets/json/shlok_data_hindi.json', 'r', encoding='utf-8') as f:
    hindi = json.load(f)

print('Entries with missing fields:')
missing = []
for idx, entry in enumerate(hindi[1:], 1):
    if not entry.get('__2') or not str(entry.get('__2', '')).strip():
        missing.append(idx)

print(f'Total entries: {len(hindi)-1}')
print(f'Entries with missing __2: {len(missing)}')
print(f'First missing: {missing[0] if missing else "None"}')
print(f'Last missing: {missing[-1] if missing else "None"}')

# Show the first few missing
print('\nFirst 10 missing entries:')
for idx in missing[:10]:
    entry = hindi[idx]
    kw_preview = entry.get('__4', '')[:20] if entry.get('__4') else 'EMPTY'
    print(f'  Entry {idx}: Ch {entry.get("__1")}, V {entry.get("__3")}, __2={entry.get("__2")}, __4={kw_preview}')

# Check if there's a pattern - every N entries?
if len(missing) > 1:
    diffs = [missing[i+1] - missing[i] for i in range(min(20, len(missing)-1))]
    print(f'\nPattern of missing entries (first 20 diffs): {diffs}')
    avg_gap = sum(diffs) / len(diffs) if diffs else 0
    print(f'Average gap: {avg_gap:.1f}')

# Find ranges of missing entries
print('\nRanges of consecutive missing entries:')
if missing:
    ranges = []
    start = missing[0]
    end = start
    for i in range(1, len(missing)):
        if missing[i] == end + 1:
            end = missing[i]
        else:
            ranges.append((start, end))
            start = missing[i]
            end = start
    ranges.append((start, end))
    
    for start, end in ranges[:5]:
        if start == end:
            print(f'  Entry {start}')
        else:
            print(f'  Entries {start}-{end} ({end-start+1} entries)')
