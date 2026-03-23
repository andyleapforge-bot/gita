import 'package:flutter/material.dart';
import '../theme/colors.dart';

class LoadingIndicator extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Center(child: CircularProgressIndicator(color: AppColors.purple));
  }
}
