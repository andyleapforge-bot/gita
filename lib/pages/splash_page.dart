import 'dart:async';
import 'package:flutter/material.dart';
import 'package:firebase_auth/firebase_auth.dart';
import '../routes.dart';

class SplashPage extends StatefulWidget {
  @override
  _SplashPageState createState() => _SplashPageState();
}

class _SplashPageState extends State<SplashPage> {
  @override
  void initState() {
    super.initState();
    // Brief splash, then route based on auth state.
    Timer(const Duration(seconds: 2), () async {
      if (!mounted) return;
      // Allow guest access to non-account features.
      Navigator.pushReplacementNamed(context, Routes.home);
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: Center(
        child: Transform.scale(
          scale: 1.02,
          child: Image.asset(
            'assets/splash/splash_screen.png',
            fit: BoxFit.contain,
          ),
        ),
      ),
    );
  }
}
