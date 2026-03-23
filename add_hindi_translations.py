import json

# Load the JSON
with open('assets/json/shlok_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Hindi chapter translations
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

# Process all shloks
processed = 0
added_translations = 0

for item in data[1:]:  # Skip header row
    if '__2' in item:
        chapter_name = item['__2']
        if chapter_name in chapter_translations and '__2_hi' not in item:
            item['__2_hi'] = chapter_translations[chapter_name]
            added_translations += 1
        processed += 1

# Save the updated JSON
with open('assets/json/shlok_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Processed: {processed} shloks")
print(f"Added Hindi translations: {added_translations}")
print("JSON updated successfully!")
