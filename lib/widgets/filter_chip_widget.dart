import 'package:flutter/material.dart';
import '../theme/colors.dart';

class FilterChipWidget extends StatelessWidget {
  final String label;
  final VoidCallback onTap;
  final bool selected;
  FilterChipWidget(
      {required this.label, required this.onTap, this.selected = false});

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        // Consistent horizontal padding; fixed vertical height via constraints
        padding: EdgeInsets.symmetric(horizontal: 16, vertical: 8),
        constraints: BoxConstraints(minHeight: 40),
        decoration: BoxDecoration(
          color:
              selected ? AppColors.badgeBackground : AppColors.chipBackground,
          borderRadius: BorderRadius.circular(25),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withOpacity(0.05),
              blurRadius: 4,
              offset: Offset(0, 2),
            ),
          ],
        ),
        child: Center(
          child: FittedBox(
            fit: BoxFit.scaleDown,
            child: Text(
              label,
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
              textAlign: TextAlign.center,
              style: TextStyle(
                color: selected ? AppColors.badgeText : AppColors.chipText,
                fontSize: 16, // base size; FittedBox will reduce if needed
                fontWeight: FontWeight.w500,
              ),
            ),
          ),
        ),
      ),
    );
  }
}
