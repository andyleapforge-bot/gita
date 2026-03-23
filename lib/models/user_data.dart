import 'package:cloud_firestore/cloud_firestore.dart';

class UserData {
  final String uid;
  final String name;
  final String email;
  final String dob;
  final List<String> bookmarks;
  final int points;
  final int rewardScore;
  final Timestamp createdAt;

  UserData({
    required this.uid,
    required this.name,
    required this.email,
    required this.dob,
    required this.bookmarks,
    required this.points,
    required this.rewardScore,
    required this.createdAt,
  });

  factory UserData.fromMap(String uid, Map<String, dynamic> map) {
    return UserData(
      uid: uid,
      name: (map['name'] ?? '') as String,
      email: (map['email'] ?? '') as String,
      dob: (map['dob'] ?? '') as String,
      bookmarks: List<String>.from(map['bookmarks'] ?? const []),
      points: (map['points'] ?? 0) is int ? map['points'] as int : 0,
      rewardScore: (map['rewardScore'] ?? map['points'] ?? 0) is int
          ? (map['rewardScore'] ?? map['points']) as int
          : 0,
      createdAt: (map['createdAt'] is Timestamp)
          ? map['createdAt'] as Timestamp
          : Timestamp.now(),
    );
  }

  Map<String, dynamic> toMap() {
    return {
      'name': name,
      'email': email,
      'dob': dob,
      'bookmarks': bookmarks,
      'points': points,
      'rewardScore': rewardScore,
      'createdAt': createdAt,
    };
  }
}
