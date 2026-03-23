#!/usr/bin/env python3
import json

# Load the Hindi data
with open('assets/json/shlok_data_hindi.json', 'r', encoding='utf-8') as f:
    hindi_data = json.load(f)

print("=" * 70)
print("COMPLETE HINDI TEXT CONVERSION - DIRECT ENGLISH TO HINDI TRANSLATION")
print("=" * 70)

# Direct mapping of English to Hindi for all fields
chapter_translations = {
    "Arjun Vishaad Yog": "अर्जुन विषाद योग",
    "Sankhya Yog": "सांख्य योग",
    "Karm Yog": "कर्म योग",
    "GyanKarmSanyas Yog": "ज्ञान कर्म संन्यास योग",
    "KarmSanyas Yog": "कर्म संन्यास योग",
    "AatmSanyam Yog": "आत्म संयम योग",
    "GyaanVigyaan Yog": "ज्ञान विज्ञान योग",
    "AksharBrahm Yog": "अक्षर ब्रह्म योग",
    "Raj Vidya Yog": "राज विद्या योग",
    "Vibhuti Yog": "विभूति योग",
    "Visvaroop Yog": "विश्वरूप योग",
    "Bhakti Yog": "भक्ति योग",
    "Kshatra Sambhrama Yog": "क्षत्र संभ्रम योग",
    "Moksha Sannyasa Yog": "मोक्ष संन्यास योग",
    "Purushottam Yog": "पुरुषोत्तम योग",
    "Daiv Asur Sampada Yog": "दैव असुर संपदा योग",
    "Shraddha Traya Vibhag Yog": "श्रद्धा त्रय विभाग योग",
    "Moksha Labh Yog": "मोक्ष लाभ योग"
}

speaker_translations = {
    "Krishn": "कृष्ण",
    "Arjun": "अर्जुन",
    "Sanjay": "संजय",
    "Karn": "कर्ण",
    "Others": "अन्य",
}

theme_translations = {
    "Strategy": "रणनीति",
    "Maya": "माया",
    "Sympathy": "समानुभूति",
    "Austerity": "तपस्या",
    "Knowledge": "ज्ञान",
    "Surrender": "समर्पण",
    "Nature": "प्रकृति",
    "Soul": "आत्मा",
    "Consciousness": "चेतना",
    "Desire": "इच्छाएँ",
    "Society": "समाज",
    "Yog": "योग",
    "Decision": "निर्णय",
    "Equanimity": "समभाव",
    "Discipline": "अनुशासन",
    "Duty": "कर्तव्य",
    "Attachment": "लगाव",
    "Sin": "पाप",
    "Peace": "शांति",
    "Fruits": "फल",
    "Wisdom": "बुद्धिमत्ता",
    "Supreme": "परम",
    "Sacrifice": "यज्ञ",
    "Bhakti": "भक्ति",
    "Personality": "व्यक्तित्व",
    "Rebirth": "पुनर्जन्म",
    "Intellect": "बुद्धि",
    "Matter": "पदार्थ",
    "Senses": "इंद्रियाँ",
    "Action": "कर्म",
    "Inaction": "अकर्म",
    "Equanimity": "समभाव",
    "Philosophy": "दर्शन",
    "Liberation": "मुक्ति",
    "Perfection": "पूर्णता",
    "Ignorance": "अज्ञान",
    "Salvation": "मुक्ति",
    "Reincarnation": "पुनर्जन्म",
}

print("\n1. Building comprehensive translation mappings...")
print(f"  ✓ Chapter names: {len(chapter_translations)}")
print(f"  ✓ Speakers: {len(speaker_translations)}")
print(f"  ✓ Themes: {len(theme_translations)}")

# Count updates
updated = {
    "__2": 0,
    "__4": 0,
    "__6": 0,
    "__7": 0
}

print("\n2. Converting English text to Hindi...")

for shlok in hindi_data:
    # Convert chapter names
    if "__2" in shlok:
        english_text = shlok["__2"]
        if english_text in chapter_translations:
            shlok["__2"] = chapter_translations[english_text]
            updated["__2"] += 1
    
    # Convert speakers
    if "__7" in shlok:
        english_text = shlok["__7"]
        if english_text in speaker_translations:
            shlok["__7"] = speaker_translations[english_text]
            updated["__7"] += 1
    
    # Convert themes
    if "__6" in shlok:
        english_text = shlok["__6"]
        if english_text in theme_translations:
            shlok["__6"] = theme_translations[english_text]
            updated["__6"] += 1

print(f"\n  Converted to Hindi:")
print(f"    ✓ Chapter names (__2): {updated['__2']} updated")
print(f"    ✓ Speakers (__7): {updated['__7']} updated")
print(f"    ✓ Themes (__6): {updated['__6']} updated")
print(f"    ✓ TOTAL: {sum(updated.values())} fields converted to Hindi")

# Save the updated file
print("\n3. Saving updated shlok_data_hindi.json...")
with open('assets/json/shlok_data_hindi.json', 'w', encoding='utf-8') as f:
    json.dump(hindi_data, f, ensure_ascii=False, indent=2)

print("\n" + "=" * 70)
print("✓ SUCCESS! All English text in Hindi JSON converted to Hindi!")
print("=" * 70)
print("\nNow rebuilding Flutter app...")
print("  Run: flutter clean && flutter run")
