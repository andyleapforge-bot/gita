class UserModel {
  final String uid;
  final String firstName;
  final String lastName;
  final String email;
  final String dob; // ISO or custom
  final List<String> bookmarks;

  UserModel({
    required this.uid,
    required this.firstName,
    required this.lastName,
    required this.email,
    required this.dob,
    required this.bookmarks,
  });

  Map<String, dynamic> toMap() => {
        'firstName': firstName,
        'lastName': lastName,
        'email': email,
        'dob': dob,
        'bookmarks': bookmarks,
      };

  factory UserModel.fromMap(String uid, Map<String, dynamic> data) {
    return UserModel(
      uid: uid,
      firstName: data['firstName'] ?? '',
      lastName: data['lastName'] ?? '',
      email: data['email'] ?? '',
      dob: data['dob'] ?? '',
      bookmarks: List<String>.from(data['bookmarks'] ?? []),
    );
  }
}
