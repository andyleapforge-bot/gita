import 'dart:convert';
import 'package:flutter/services.dart' show rootBundle;

class VideoService {
  static const String _path = 'assets/video_links.json';

  Future<List<String>> getVideosForShlok(String shlokId) async {
    final raw = await rootBundle.loadString(_path);
    final data = json.decode(raw) as Map<String, dynamic>;
    final vids = data[shlokId];
    if (vids is List) {
      return vids.map((e) => e.toString()).toList();
    }
    return const [];
  }
}
