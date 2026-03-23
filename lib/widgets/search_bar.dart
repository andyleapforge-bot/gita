import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../theme/colors.dart';
import '../services/language_service.dart';
import '../services/localization_service.dart';

class VitaSearchBar extends StatelessWidget {
  final ValueChanged<String> onChanged;
  VitaSearchBar({required this.onChanged});

  @override
  Widget build(BuildContext context) {
    final langService = Provider.of<LanguageService>(context, listen: false);
    return Container(
      decoration: BoxDecoration(
        color: AppColors.searchBarBackground,
        borderRadius: BorderRadius.circular(30),
        border: Border.all(color: AppColors.searchBorder, width: 1.5),
      ),
      padding: EdgeInsets.symmetric(horizontal: 16, vertical: 4),
      child: Row(
        children: [
          Icon(Icons.search, color: AppColors.navy, size: 24),
          SizedBox(width: 12),
          Expanded(
            child: TextField(
              decoration: InputDecoration(
                border: InputBorder.none,
                hintText: LocalizationService.translate(
                    'search', langService.language),
                hintStyle: TextStyle(
                  color: AppColors.summaryText.withOpacity(0.6),
                  fontSize: 16,
                ),
              ),
              style: TextStyle(color: AppColors.titleText, fontSize: 16),
              onChanged: onChanged,
            ),
          ),
        ],
      ),
    );
  }
}
