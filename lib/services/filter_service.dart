import 'package:cloud_firestore/cloud_firestore.dart';
import '../models/filter_option.dart';

class FilterService {
  final FirebaseFirestore _db = FirebaseFirestore.instance;

  Future<List<FilterOption>> getFilterOptions(String collection) async {
    final snap = await _db.collection(collection).get();
    return snap.docs.map((d) => FilterOption.fromMap(d.id, d.data())).toList();
  }
}
