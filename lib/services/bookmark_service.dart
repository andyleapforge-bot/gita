import 'package:cloud_firestore/cloud_firestore.dart';

class BookmarkService {
  final FirebaseFirestore _db = FirebaseFirestore.instance;

  Future<void> addBookmark(String uid, String shlokId) async {
    final ref = _db.collection('users').doc(uid);
    try {
      await ref.set({
        'bookmarks': FieldValue.arrayUnion([shlokId])
      }, SetOptions(merge: true));
    } catch (_) {}
  }

  Future<void> removeBookmark(String uid, String shlokId) async {
    final ref = _db.collection('users').doc(uid);
    try {
      await ref.update({
        'bookmarks': FieldValue.arrayRemove([shlokId])
      });
    } catch (_) {}
  }

  Future<List<String>> getUserBookmarks(String uid) async {
    try {
      final doc = await _db.collection('users').doc(uid).get();
      if (!doc.exists) return [];
      final data = doc.data();
      return List<String>.from(data?['bookmarks'] ?? []);
    } catch (_) {
      return [];
    }
  }
}
