import 'package:flutter/material.dart';
import 'colors.dart';

class TextStyles {
  static final TextStyle title = TextStyle(
    fontSize: 18,
    fontWeight: FontWeight.bold,
    color: AppColors.navy,
  );

  static final TextStyle subtitle = TextStyle(
    fontSize: 14,
    color: AppColors.navy,
  );

  static final TextTheme textTheme = TextTheme(
    titleLarge: title,
    titleMedium: subtitle,
    bodyMedium: TextStyle(fontSize: 14, color: AppColors.navy),
  );
}
