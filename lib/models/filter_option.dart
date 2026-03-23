class FilterOption {
  final String id;
  final String name;

  FilterOption({required this.id, required this.name});

  factory FilterOption.fromMap(String id, Map<String, dynamic> data) {
    return FilterOption(id: id, name: data['name'] ?? '');
  }
}
