import 'package:flutter/material.dart';

class LanguageService extends ChangeNotifier {
  static final LanguageService _instance = LanguageService._internal();

  factory LanguageService() {
    return _instance;
  }

  LanguageService._internal();

  String _language = 'en'; // 'en' or 'hi'

  String get language => _language;

  void setLanguage(String lang) {
    if (_language != lang) {
      _language = lang;
      notifyListeners();
    }
  }

  // English translations
  static const Map<String, String> enTranslations = {
    'bookmarks': 'Bookmarks',
    'profile': 'Profile',
    'gamification': 'Rewards',
    'your_points': 'Your Points',
    'language': 'Language',
    'english': 'English',
    'hindi': 'हिंदी',
    'showing_results': 'Showing %d results',
    'clear_filters': 'Clear filters',
    'no_shloks': 'No shloks found',
    'theme': 'Theme',
    'speaker': 'Speaker',
    'stars': 'Stars',
    'chapter': 'Chapter',
    'shlok_number': 'Shlok Number',
    'filter_by': 'Filter by %s',
    'clear': 'Clear',
    'cancel': 'Cancel',
    'apply': 'Apply',
  };

  // Hindi translations
  static const Map<String, String> hiTranslations = {
    'bookmarks': 'बुकमार्क्स',
    'profile': 'प्रोफाइल',
    'gamification': 'इनाम',
    'your_points': 'आपके अंक',
    'language': 'भाषा',
    'english': 'English',
    'hindi': 'हिंदी',
    'showing_results': '%d परिणाम दिखाए जा रहे हैं',
    'clear_filters': 'फ़िल्टर साफ़ करें',
    'no_shloks': 'कोई श्लोक नहीं मिला',
    'theme': 'विषय',
    'speaker': 'वक्ता',
    'stars': 'श्रेणी',
    'chapter': 'अध्याय',
    'shlok_number': 'श्लोक संख्या',
    'filter_by': '%s के अनुसार फ़िल्टर करें',
    'clear': 'साफ़ करें',
    'cancel': 'रद्द करें',
    'apply': 'लागू करें',
  };

  String translate(String key, [int? count]) {
    final map = _language == 'hi' ? hiTranslations : enTranslations;
    final text = map[key] ?? key;
    if (count != null) {
      return text.replaceAll('%d', count.toString());
    }
    return text;
  }

  String translateWithParam(String key, String param) {
    final map = _language == 'hi' ? hiTranslations : enTranslations;
    final text = map[key] ?? key;
    return text.replaceAll('%s', param);
  }
}
