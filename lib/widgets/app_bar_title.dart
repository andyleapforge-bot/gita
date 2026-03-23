import 'package:flutter/material.dart';
import '../theme/colors.dart';

class AppBarTitle extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return SizedBox(
      height: kToolbarHeight,
      width: 360, // maximize visual size within AppBar constraints
      child: Align(
        alignment: Alignment.centerLeft,
        child: Image.asset(
          'assets/splash/FINAL_NAVLOGO.png',
          fit: BoxFit.fitHeight,
        ),
      ),
    );
  }
}
