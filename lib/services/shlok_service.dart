import 'dart:convert';
import 'package:flutter/services.dart';
import '../models/shlok.dart';

class ShlokService {
  List<Shlok>? _cacheEnglish;
  List<Shlok>? _cacheHindi;
  String _currentLanguage = 'en';

  Future<List<Shlok>> getAllShloks({String language = 'en'}) async {
    _currentLanguage = language;

    if (language == 'hi') {
      if (_cacheHindi != null) return _cacheHindi!;

      final raw =
          await rootBundle.loadString('assets/json/shlok_data_hindi.json');
      final List<dynamic> jsonList = jsonDecode(raw);

      _cacheHindi = jsonList
          .skip(1)
          .where((item) => item['__1'] != null && item['__1'] != '')
          .map<Shlok>((e) => Shlok.fromJson(e))
          .where((s) => s.title.isNotEmpty)
          .toList();

      return _cacheHindi!;
    } else {
      // Default to English
      if (_cacheEnglish != null) return _cacheEnglish!;

      final raw = await rootBundle.loadString('assets/json/shlok_data.json');
      final List<dynamic> jsonList = jsonDecode(raw);

      _cacheEnglish = jsonList
          .skip(1)
          .where((item) => item['__1'] != null && item['__1'] != '')
          .map<Shlok>((e) => Shlok.fromJson(e))
          .where((s) => s.title.isNotEmpty)
          .toList();

      return _cacheEnglish!;
    }
  }

  Future<Shlok?> getShlokById(String id, {String language = 'en'}) async {
    final all = await getAllShloks(language: language);
    try {
      return all.firstWhere((s) => s.id == id);
    } catch (e) {
      return null;
    }
  }

  Future<List<Shlok>> searchShloks(String query,
      {String language = 'en'}) async {
    final all = await getAllShloks(language: language);
    final q = query.toLowerCase();
    return all.where((s) {
      return s.title.toLowerCase().contains(q) ||
          s.summary.toLowerCase().contains(q) ||
          s.keywords.any((k) => k.toLowerCase().contains(q));
    }).toList();
  }

  Future<List<Shlok>> getFilteredShloks(Map<String, dynamic> filters,
      {String language = 'en'}) async {
    final all = await getAllShloks(language: language);
    return all.where((shlok) {
      for (var entry in filters.entries) {
        if (entry.value == null) continue;
        switch (entry.key) {
          case 'chapter':
            if (shlok.chapter != entry.value) return false;
            break;
          case 'speaker':
            if (shlok.speaker != entry.value) return false;
            break;
          case 'theme':
            if (shlok.theme != entry.value) return false;
            break;
          case 'star':
            if (shlok.star != entry.value) return false;
            break;
        }
      }
      return true;
    }).toList();
  }
}
