import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_auth/firebase_auth.dart';
import '../models/user_data.dart';

class UserService {
  static const String usersCollection = 'users';
  final FirebaseFirestore _db = FirebaseFirestore.instance;

  /// FIXED: No .get() — only writes are allowed by your rules.
  Future<void> createUserIfNotExists(UserCredential user) async {
    final u = user.user;
    if (u == null) return;

    final ref = _db.collection(usersCollection).doc(u.uid);

    await ref.set({
      'name': '',
      'email': u.email ?? '',
      'dob': '',
      'bookmarks': <String>[],
      'points': 0,
      'rewardScore': 0,
      'streak': 0,
      'lastOpenDate': '',
      'createdAt': Timestamp.now(),
    }, SetOptions(merge: true));
  }

  Future<UserData?> getUserData(String uid) async {
    // This still REQUIRES your Firestore rules to allow read
    final doc = await _db.collection(usersCollection).doc(uid).get();
    if (!doc.exists) return null;
    return UserData.fromMap(uid, doc.data() ?? {});
  }

  Future<void> updateName(String uid, String newName) async {
    await _db.collection(usersCollection).doc(uid).update({'name': newName});
  }

  Future<void> updateDob(String uid, String newDob) async {
    await _db.collection(usersCollection).doc(uid).update({'dob': newDob});
  }

  /// Ensure points fields exist on the user document (for older accounts).
  Future<void> ensurePointsFields(String uid) async {
    await _db.collection(usersCollection).doc(uid).set({
      'points': FieldValue.increment(0),
      'rewardScore': FieldValue.increment(0),
      'activities': {},
    }, SetOptions(merge: true));
  }

  /// Check if an activity was already awarded today (by date key YYYY-MM-DD).
  Future<bool> isActivityEligibleToday(String uid, String activityName) async {
    final dateKey =
        DateTime.now().toIso8601String().split('T').first; // YYYY-MM-DD
    final doc = await _db.collection(usersCollection).doc(uid).get();
    if (!doc.exists) return true;
    final activities =
        (doc.data()?['activities'] as Map<String, dynamic>?) ?? {};
    final actKey = '$activityName:$dateKey';
    return !activities.containsKey(actKey);
  }

  /// Log an activity and award points if eligible (for daily-capped activities).
  Future<void> logActivityAndAwardPoints(
    String uid,
    String activityName,
    int pointsToAward,
  ) async {
    final dateKey =
        DateTime.now().toIso8601String().split('T').first; // YYYY-MM-DD
    final actKey = '$activityName:$dateKey';

    await _db.collection(usersCollection).doc(uid).set({
      'points': FieldValue.increment(pointsToAward),
      'rewardScore': FieldValue.increment(pointsToAward),
      'activities.$actKey': FieldValue.serverTimestamp(),
    }, SetOptions(merge: true));
  }

  /// Log a listen activity (no daily cap - award points every time user listens to completion).
  /// Each unique shlok can award points multiple times.
  Future<void> logListenActivityAndAwardPoints(
    String uid,
    String shlokId,
    int pointsToAward,
  ) async {
    final actKey = 'listen:$shlokId';

    await _db.collection(usersCollection).doc(uid).set({
      'points': FieldValue.increment(pointsToAward),
      'rewardScore': FieldValue.increment(pointsToAward),
      'activities.$actKey': FieldValue.serverTimestamp(),
    }, SetOptions(merge: true));
  }

  /// Get raw user doc data (for checking activities).
  Future<Map<String, dynamic>?> getDoc(String uid) async {
    final doc = await _db.collection(usersCollection).doc(uid).get();
    if (!doc.exists) return null;
    return doc.data();
  }

  Future<void> addBookmark(String uid, String shlokId) async {
    await _db.collection(usersCollection).doc(uid).update({
      'bookmarks': FieldValue.arrayUnion([shlokId])
    });
  }

  Future<void> removeBookmark(String uid, String shlokId) async {
    await _db.collection(usersCollection).doc(uid).update({
      'bookmarks': FieldValue.arrayRemove([shlokId])
    });
  }

  Future<bool> isBookmarked(String uid, String shlokId) async {
    final data = await getUserData(uid);
    if (data == null) return false;
    return data.bookmarks.contains(shlokId);
  }

  Future<List<String>> getBookmarks(String uid) async {
    final data = await getUserData(uid);
    return data?.bookmarks ?? <String>[];
  }

  Future<int> getPoints(String uid) async {
    final doc = await _db.collection(usersCollection).doc(uid).get();
    if (!doc.exists) return 0;
    final data = doc.data() ?? {};
    final pts = data['points'] ?? data['rewardScore'];
    if (pts is int) return pts;
    if (pts is num) return pts.toInt();
    return 0;
  }

  Future<void> setPoints(String uid, int points) async {
    await _db.collection(usersCollection).doc(uid).set(
        {'points': points, 'rewardScore': points}, SetOptions(merge: true));
  }

  Future<void> incrementPoints(String uid, int delta) async {
    await _db.collection(usersCollection).doc(uid).set({
      'points': FieldValue.increment(delta),
      'rewardScore': FieldValue.increment(delta),
    }, SetOptions(merge: true));
  }

  /// Update streak: check if user opened app consecutively
  Future<int> updateStreak(String uid) async {
    final now = DateTime.now();
    final today = DateTime(now.year, now.month, now.day);
    final todayKey = today.toIso8601String().split('T').first;

    final doc = await _db.collection(usersCollection).doc(uid).get();
    if (!doc.exists) return 0;

    final data = doc.data() ?? {};
    final lastOpenStr = data['lastOpenDate'] as String?;
    final currentStreak = (data['streak'] as num?)?.toInt() ?? 0;

    if (lastOpenStr == null) {
      // First time opening
      await _db.collection(usersCollection).doc(uid).set({
        'streak': 1,
        'lastOpenDate': todayKey,
      }, SetOptions(merge: true));
      return 1;
    }

    final lastOpen = DateTime.parse(lastOpenStr);
    final lastOpenDate = DateTime(lastOpen.year, lastOpen.month, lastOpen.day);
    final daysDiff = today.difference(lastOpenDate).inDays;

    if (daysDiff == 0) {
      // Same day - no change
      return currentStreak;
    } else if (daysDiff == 1) {
      // Consecutive day - increment streak
      final newStreak = currentStreak + 1;
      await _db.collection(usersCollection).doc(uid).set({
        'streak': newStreak,
        'lastOpenDate': todayKey,
      }, SetOptions(merge: true));
      return newStreak;
    } else {
      // Missed a day - reset streak
      await _db.collection(usersCollection).doc(uid).set({
        'streak': 1,
        'lastOpenDate': todayKey,
      }, SetOptions(merge: true));
      return 1;
    }
  }

  /// Get current streak
  Future<int> getStreak(String uid) async {
    final doc = await _db.collection(usersCollection).doc(uid).get();
    if (!doc.exists) return 0;
    final data = doc.data() ?? {};
    return (data['streak'] as num?)?.toInt() ?? 0;
  }
}
