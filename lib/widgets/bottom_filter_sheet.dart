import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../theme/colors.dart';
import '../services/language_service.dart';

class BottomFilterSheet extends StatelessWidget {
  final String title;
  final VoidCallback onApply;
  final VoidCallback onClear;

  BottomFilterSheet(
      {required this.title, required this.onApply, required this.onClear});

  @override
  Widget build(BuildContext context) {
    final langService = Provider.of<LanguageService>(context);
    return Container(
      padding: EdgeInsets.all(16),
      child: Column(mainAxisSize: MainAxisSize.min, children: [
        Row(mainAxisAlignment: MainAxisAlignment.spaceBetween, children: [
          Text(title, style: TextStyle(fontSize: 18, color: AppColors.navy)),
          TextButton(
              onPressed: onClear, child: Text(langService.translate('clear'))),
        ]),
        SizedBox(height: 8),
        // Placeholder for checkbox list
        Column(children: [
          CheckboxListTile(
              value: false, onChanged: (v) {}, title: Text('Option 1'))
        ]),
        SizedBox(height: 12),
        Row(mainAxisAlignment: MainAxisAlignment.end, children: [
          TextButton(
              onPressed: () => Navigator.pop(context),
              child: Text(langService.translate('cancel'))),
          ElevatedButton(
              onPressed: onApply, child: Text(langService.translate('apply'))),
        ])
      ]),
    );
  }
}
