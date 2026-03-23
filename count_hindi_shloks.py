import json

with open('assets/json/shlok_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

total_shloks = len(data) - 1
shloks_with_chapter_hi = 0
shloks_with_speaker_hi = 0
shloks_with_theme_hi = 0
shloks_with_keywords_hi = 0

for shlok in data[1:]:
    if '__2_hi' in shlok and shlok['__2_hi']:
        shloks_with_chapter_hi += 1
    if '__7_hi' in shlok and shlok['__7_hi']:
        shloks_with_speaker_hi += 1
    if '__6_hi' in shlok and shlok['__6_hi']:
        shloks_with_theme_hi += 1
    if '__4_hi' in shlok and shlok['__4_hi']:
        shloks_with_keywords_hi += 1

print('='*60)
print('HINDI TRANSLATION STATISTICS')
print('='*60)
print(f'Total Shloks in Database: {total_shloks}')
print()
print('Hindi Translations Added:')
print(f'  ✓ Chapter Names: {shloks_with_chapter_hi} shloks')
print(f'  ✓ Speaker Names: {shloks_with_speaker_hi} shloks')
print(f'  ✓ Theme Names: {shloks_with_theme_hi} shloks')
print(f'  ✓ Keywords: {shloks_with_keywords_hi} shloks')
print()
print(f'Coverage:')
print(f'  • Chapter: {(shloks_with_chapter_hi/total_shloks)*100:.1f}%')
print(f'  • Speakers: {(shloks_with_speaker_hi/total_shloks)*100:.1f}%')
print(f'  • Themes: {(shloks_with_theme_hi/total_shloks)*100:.1f}%')
print(f'  • Keywords: {(shloks_with_keywords_hi/total_shloks)*100:.1f}%')
print('='*60)
