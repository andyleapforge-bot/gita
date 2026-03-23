import json

# Load both versions
with open('assets/json/shlok_data.json', 'r', encoding='utf-8') as f:
    english = json.load(f)

with open('assets/json/shlok_data_hindi.json', 'r', encoding='utf-8') as f:
    hindi = json.load(f)

print('=== VERIFICATION: ENGLISH vs HINDI ===\n')

print(f'Entry count: EN {len(english)-1}, HI {len(hindi)-1}')
print(f'Headers match: {english[0]["__4"] == hindi[0]["__4"]}\n')

# Compare field completeness
def check_completeness(data, name):
    counts = {f'__{i}': 0 for i in range(1, 10)}
    for entry in data[1:]:  # Skip header
        for field in ['__1', '__2', '__3', '__4', '__5', '__6', '__7', '__8', '__9']:
            val = entry.get(field, '')
            if val and str(val).strip():
                counts[field] += 1
    print(f'{name} field completeness:')
    for field in ['__1', '__2', '__3', '__4', '__5', '__6', '__7', '__8', '__9']:
        print(f'  {field}: {counts[field]}/{len(data)-1}')
    return counts

en_counts = check_completeness(english, 'ENGLISH')
print()
hi_counts = check_completeness(hindi, 'HINDI')

print('\n=== FIELD-BY-FIELD COMPARISON ===')
for field in ['__1', '__2', '__3', '__4', '__5', '__6', '__7', '__8', '__9']:
    en_val = en_counts[field]
    hi_val = hi_counts[field]
    status = '✅' if en_val == hi_val else ('⚠️' if abs(en_val - hi_val) <= 5 else '❌')
    print(f'{field}: {status} EN {en_val}/700 vs HI {hi_val}/700')

print('\n=== SAMPLE ENTRY COMPARISON ===')
for idx in [1, 2, 50, 100, 200]:
    print(f'\n--- Entry {idx} ---')
    print(f'EN - Ch {english[idx]["__1"]}, V {english[idx]["__3"]}, Star {english[idx]["__5"]}')
    print(f'    Keywords: {english[idx]["__4"][:60]}')
    print(f'HI - Ch {hindi[idx]["__1"]}, V {hindi[idx]["__3"]}, Star {hindi[idx]["__5"]}')
    print(f'    Keywords: {hindi[idx]["__4"][:60]}')

# Check if data can be properly loaded by the app
print('\n=== APP COMPATIBILITY CHECK ===')
errors = 0
warnings = 0

for idx, entry in enumerate(hindi[1:], 1):
    # Check if required fields exist and are non-empty
    if not entry.get('__1') or entry['__1'] <= 0:
        print(f'❌ Entry {idx}: Missing chapter')
        errors += 1
    if not entry.get('__3') or entry['__3'] <= 0:
        print(f'❌ Entry {idx}: Missing verse number')
        errors += 1
    if not entry.get('__4'):
        print(f'⚠️ Entry {idx}: Missing keywords')
        warnings += 1
    if entry.get('__5', 0) == 0:
        print(f'⚠️ Entry {idx}: Star rating is 0')
        if warnings > 10:
            print('  (... more warnings omitted)')
            break
        warnings += 1

if errors == 0 and warnings <= 10:
    print('✅ All entries have required fields!')
elif errors == 0:
    print(f'⚠️ {warnings} entries have empty/zero optional fields (may affect filtering)')
else:
    print(f'❌ {errors} critical errors found!')
