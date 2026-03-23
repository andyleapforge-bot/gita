import 'package:flutter/material.dart';
import 'pages/splash_page.dart';
import 'pages/signup_page.dart';
import 'pages/login_page.dart';
import 'pages/home_page.dart';
import 'pages/shlok_detail_page.dart';
import 'pages/bookmarks_page.dart';
import 'pages/profile_page.dart';
import 'pages/gamification_page.dart';

class Routes {
  static const splash = '/';
  static const signup = '/signup';
  static const login = '/login';
  static const home = '/home';
  static const shlokDetail = '/shlok';
  static const bookmarks = '/bookmarks';
  static const profile = '/profile';
  static const gamification = '/gamification';

  static Map<String, WidgetBuilder> getRoutes() => {
        splash: (_) => SplashPage(),
        signup: (_) => SignUpPage(),
        login: (_) => LoginPage(),
        home: (_) => HomePage(),
        shlokDetail: (_) => ShlokDetailPage(),
        bookmarks: (_) => BookmarksPage(),
        profile: (_) => ProfilePage(),
        gamification: (_) => GamificationPage(),
      };
}
