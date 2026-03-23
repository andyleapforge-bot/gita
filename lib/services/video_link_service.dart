import 'dart:convert';
import 'package:flutter/services.dart';
import '../models/shlok.dart';

class VideoLinkService {
  Map<String, String>? _cache;

  Future<Map<String, String>> _loadLinks() async {
    if (_cache != null) return _cache!;
    final raw = await rootBundle.loadString('assets/json/video_links.json');
    final Map<String, dynamic> data = jsonDecode(raw);
    _cache = data.map((k, v) => MapEntry(k.toString(), v.toString()));
    return _cache!;
  }

  String _formatNumber(double n) {
    if (n % 1 == 0) return n.toInt().toString();
    var s = n.toString();
    if (s.contains('.')) {
      s = s.replaceAll(RegExp(r'0+$'), '');
      if (s.endsWith('.')) {
        s = s.substring(0, s.length - 1);
      }
    }
    return s;
  }

  Future<String?> getVideoUrlForShlok(Shlok shlok) async {
    final links = await _loadLinks();
    final chap = shlok.chapter.toString();
    final numStr = _formatNumber(shlok.number);
    final pattern = ' $chap.$numStr.mp4';

    // Find first key that ends with the pattern
    for (final entry in links.entries) {
      if (entry.key.endsWith(pattern)) {
        return entry.value;
      }
    }
    return null;
  }
}
