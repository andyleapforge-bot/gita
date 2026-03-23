import json
from datetime import datetime

# Load the JSON
with open('assets/json/shlok_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Hindi translations for all chapters, speakers, themes, keywords
chapter_translations = {
    'Arjun Vishaad Yog': 'अर्जुन विषाद योग',
    'Sankhya Yog': 'साँख्य योग',
    'Karma Yog': 'कर्म योग',
    'Gnan Yog': 'ज्ञान योग',
    'Bhakti Yog': 'भक्ति योग',
    'Aatma Samyam Yog': 'आत्मसंयम योग',
    'Gnan Vigyan Yog': 'ज्ञान विज्ञान योग',
    'Akshara Brahm Yog': 'अक्षर ब्रह्म योग',
    'Raaj Vidya Yog': 'राज विद्या योग',
    'Vibhuti Yog': 'विभूति योग',
    'Vishwarup Darshan Yog': 'विश्वरूप दर्शन योग',
    'Kshetra Kshetragya Vibhag Yog': 'क्षेत्र क्षेत्रज्ञ विभाग योग',
    'Guna Traya Vibhag Yog': 'गुण त्रय विभाग योग',
    'Purushotam Yog': 'पुरुषोत्तम योग',
    'Daivasur Sampad Vibhag Yog': 'दैवासुर संपद विभाग योग',
    'Shraddha Traya Vibhag Yog': 'श्रद्धा त्रय विभाग योग',
    'Moksh Sannyaas Yog': 'मोक्ष संन्यास योग',
}

speaker_translations = {
    'Dhritrashtr': 'धृतराष्ट्र',
    'Sanjay': 'संजय',
    'Duryodhan': 'दुर्योधन',
    'Arjun': 'अर्जुन',
    'Krishna': 'कृष्ण',
    'Kaurav': 'कौरव',
}

theme_translations = {
    'Strategy': 'रणनीति',
    'Discipline': 'अनुशासन',
    'Knowledge': 'ज्ञान',
    'Action': 'कर्म',
    'Devotion': 'भक्ति',
    'Wisdom': 'बुद्धिमत्ता',
    'Yoga': 'योग',
    'Renunciation': 'संन्यास',
    'Meditation': 'ध्यान',
    'Self': 'आत्मा',
    'Liberation': 'मुक्ति',
    'Soul': 'आत्मा',
    'Courage': 'साहस',
}

keyword_translations = {
    'Dharmkshetr': 'धर्मक्षेत्र',
    'Kurukshetr': 'कुरुक्षेत्र',
    'Curiosity': 'जिज्ञासा',
    'Vision': 'दृष्टि',
    'Observe': 'अवलोकन',
    'Prepare': 'तैयारी',
    'Enemy': 'शत्रु',
    'Consult': 'परामर्श',
    'Report': 'रिपोर्ट',
    'Revered': 'सम्मानित',
    'Master': 'गुरु',
    'Mighty': 'शक्तिशाली',
    'Arrayed': 'व्यवस्थित',
    'Army': 'सेना',
    'Battle': 'युद्ध',
    'Talented': 'प्रतिभाशाली',
    'Spirituality': 'आध्यात्मिकता',
    'Adhiyagna': 'अधियज्ञ',
    'Supreme': 'सर्वोच्च',
    'Indestructible': 'अविनाशी',
    'Brahm': 'ब्रह्म',
    'Valiant': 'वीर',
    'King': 'राजा',
    'Best': 'सर्वश्रेष्ठ',
    'Men': 'पुरुष',
    'Warrior': 'योद्धा',
    'Generals': 'जनरल',
    'Information': 'जानकारी',
    'Hero': 'नायक',
    'Military': 'सैन्य',
    'Prowess': 'पराक्रम',
    'Principal': 'प्रमुख',
}

def translate_keywords(keywords_str):
    """Translate keywords by splitting and translating each one"""
    if not keywords_str:
        return None
    keywords = keywords_str.split()
    translated = []
    for kw in keywords:
        translated.append(keyword_translations.get(kw, kw))
    return ' '.join(translated)

def translate_field(text, translation_dict):
    """Translate a field using the provided dictionary"""
    return translation_dict.get(text, text)

# Process all shloks
processed = 0
added_translations = 0

for item in data[1:]:  # Skip header row
    if '__2' in item:
        # Translate chapter name
        if '__2_hi' not in item:
            chapter_name = item['__2']
            if chapter_name in chapter_translations:
                item['__2_hi'] = chapter_translations[chapter_name]
                added_translations += 1
        
        # Translate speaker
        if '__7_hi' not in item and '__7' in item:
            speaker = item['__7']
            if speaker in speaker_translations:
                item['__7_hi'] = speaker_translations[speaker]
        
        # Translate theme
        if '__6_hi' not in item and '__6' in item:
            theme = item['__6']
            if theme in theme_translations:
                item['__6_hi'] = theme_translations[theme]
        
        # Translate keywords
        if '__4_hi' not in item and '__4' in item:
            keywords_translated = translate_keywords(item['__4'])
            if keywords_translated != item['__4']:  # Only add if there was a translation
                item['__4_hi'] = keywords_translated
        
        processed += 1

# Save the updated JSON
with open('assets/json/shlok_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Processing complete!")
print(f"Total shloks processed: {processed}")
print(f"Chapter name translations added: {added_translations}")
print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("\nTranslations added for:")
print("  ✓ Chapter names (__2_hi)")
print("  ✓ Speakers (__7_hi)")
print("  ✓ Themes (__6_hi)")
print("  ✓ Keywords (__4_hi)")
