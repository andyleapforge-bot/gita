import 'package:cloud_firestore/cloud_firestore.dart';
import '../services/hindi_translations.dart';

class Shlok {
  final String id;
  final int chapter;
  final double number;
  final String title;
  final String summary;
  final String speaker;
  final String theme;
  final int star;
  final List<String> keywords;
  final String sanskrit;
  final String translation;
  final String posterImageUrl;
  final String? titleHi;
  final String? summaryHi;
  final String? speakerHi;
  final String? themeHi;
  final List<String>? keywordsHi;

  Shlok({
    required this.id,
    required this.chapter,
    required this.number,
    required this.title,
    required this.summary,
    required this.speaker,
    required this.theme,
    required this.star,
    required this.keywords,
    required this.sanskrit,
    required this.translation,
    required this.posterImageUrl,
    this.titleHi,
    this.summaryHi,
    this.speakerHi,
    this.themeHi,
    this.keywordsHi,
  });

  // Get localized content - use Hindi translations as fallback
  String getLocalizedTitle(String language) {
    if (language == 'hi') {
      if (titleHi != null && titleHi!.isNotEmpty) return titleHi!;
      // No Hindi translation in database, return English for now
      return title;
    }
    return title;
  }

  String getLocalizedSummary(String language) {
    if (language == 'hi') {
      if (summaryHi != null && summaryHi!.isNotEmpty) return summaryHi!;
      return summary;
    }
    return summary;
  }

  String getLocalizedSpeaker(String language) {
    if (language == 'hi') {
      if (speakerHi != null && speakerHi!.isNotEmpty) return speakerHi!;
      // Try to translate the English speaker name
      return HindiTranslations.translateSpeaker(speaker);
    }
    return speaker;
  }

  String getLocalizedTheme(String language) {
    if (language == 'hi') {
      if (themeHi != null && themeHi!.isNotEmpty) return themeHi!;
      // Try to translate the English theme name
      return HindiTranslations.translateTheme(theme);
    }
    return theme;
  }

  List<String> getLocalizedKeywords(String language) {
    if (language == 'hi') {
      if (keywordsHi != null && keywordsHi!.isNotEmpty) return keywordsHi!;
      // Try to translate the English keywords
      return HindiTranslations.translateKeywords(keywords);
    }
    return keywords;
  }

  factory Shlok.fromFirestore(DocumentSnapshot doc) {
    final data = doc.data() as Map<String, dynamic>;
    return Shlok(
      id: doc.id,
      chapter: data['chapter'] ?? 0,
      number: (data['number'] is int)
          ? (data['number'] as int).toDouble()
          : (data['number'] ?? 0.0),
      title: data['title'] ?? '',
      summary: data['summary'] ?? '',
      speaker: data['speaker'] ?? '',
      theme: data['theme'] ?? '',
      star: data['star'] ?? 0,
      keywords: List<String>.from(data['keywords'] ?? []),
      sanskrit: data['sanskrit'] ?? '',
      translation: data['translation'] ?? '',
      posterImageUrl: data['posterImageUrl'] ?? '',
      titleHi: data['title_hi'],
      summaryHi: data['summary_hi'],
      speakerHi: data['speaker_hi'],
      themeHi: data['theme_hi'],
      keywordsHi: data['keywords_hi'] != null
          ? List<String>.from(data['keywords_hi'])
          : null,
    );
  }

  factory Shlok.fromJson(Map<String, dynamic> json) {
    final chapterNum = json['__1'];
    final shlokNum = json['__3'];
    return Shlok(
      id: '${chapterNum}_$shlokNum',
      chapter: chapterNum is int
          ? chapterNum
          : int.tryParse(chapterNum?.toString() ?? '0') ?? 0,
      number: shlokNum is int
          ? shlokNum.toDouble()
          : double.tryParse(shlokNum?.toString() ?? '0') ?? 0.0,
      title: json['__2']?.toString() ?? '',
      summary: json['__8']?.toString() ?? '',
      speaker: json['__7']?.toString() ?? '',
      theme: json['__6']?.toString() ?? '',
      star: json['__5'] is int
          ? json['__5']
          : int.tryParse(json['__5']?.toString() ?? '0') ?? 0,
      keywords: (json['__4']?.toString() ?? '')
          .split(' ')
          .where((k) => k.isNotEmpty)
          .toList(),
      sanskrit: json['sanskrit']?.toString() ?? '',
      translation: json['translation']?.toString() ?? '',
      posterImageUrl: json['posterImageUrl']?.toString() ?? '',
      titleHi: json['__2_hi']?.toString(),
      summaryHi: json['__8_hi']?.toString(),
      speakerHi: json['__7_hi']?.toString(),
      themeHi: json['__6_hi']?.toString(),
      keywordsHi: json['__4_hi'] != null
          ? (json['__4_hi'].toString())
              .split(' ')
              .where((k) => k.isNotEmpty)
              .toList()
          : null,
    );
  }
}
