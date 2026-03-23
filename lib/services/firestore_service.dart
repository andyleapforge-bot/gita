import 'package:cloud_firestore/cloud_firestore.dart';

class FirestoreService {
  final FirebaseFirestore _db = FirebaseFirestore.instance;

  CollectionReference<Map<String, dynamic>> collection(String path) =>
      _db.collection(path);

  Future<DocumentSnapshot<Map<String, dynamic>>> getDoc(
      String path, String id) {
    return collection(path).doc(id).get();
  }

  Future<void> setDoc(String path, String id, Map<String, dynamic> data) {
    return collection(path).doc(id).set(data);
  }

  Future<void> updateDoc(String path, String id, Map<String, dynamic> data) {
    return collection(path).doc(id).update(data);
  }

  Stream<QuerySnapshot<Map<String, dynamic>>> streamCollection(String path) {
    return collection(path).snapshots();
  }
}
