// Hindi translations for common shlok content
class HindiTranslations {
  static const Map<String, String> speakers = {
    'Dhritrashtr': 'धृतराष्ट्र',
    'Sanjay': 'संजय',
    'Duryodhan': 'दुर्योधन',
    'Arjun': 'अर्जुन',
    'Krishna': 'कृष्ण',
    'Kaurav': 'कौरव',
  };

  static const Map<String, String> themes = {
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
  };

  static const Map<String, String> keywords = {
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
    'Krishna': 'कृष्ण',
    'Arjun': 'अर्जुन',
  };

  static String translateSpeaker(String speaker) {
    return speakers[speaker] ?? speaker;
  }

  static String translateTheme(String theme) {
    return themes[theme] ?? theme;
  }

  static String translateKeyword(String keyword) {
    return keywords[keyword] ?? keyword;
  }

  static List<String> translateKeywords(List<String> keywordList) {
    return keywordList.map((k) => translateKeyword(k)).toList();
  }

  // Translate chapter names
  static String translateChapter(String chapterName) {
    const chapters = {
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
    };
    return chapters[chapterName] ?? chapterName;
  }
}
