import 'package:firebase_core/firebase_core.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'routes.dart';
import 'services/auth_service.dart';
import 'services/language_service.dart';
import 'theme/colors.dart';
import 'theme/text_styles.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp();
  runApp(VitaGitaApp());
}

class VitaGitaApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        Provider<AuthService>(create: (_) => AuthService()),
        ChangeNotifierProvider<LanguageService>(
          create: (_) => LanguageService(),
        ),
      ],
      child: MaterialApp(
        title: 'VitaGita',
        debugShowCheckedModeBanner: false,
        theme: ThemeData(
          primaryColor: AppColors.navy,
          scaffoldBackgroundColor: AppColors.cream,
          textTheme: TextStyles.textTheme,
          elevatedButtonTheme: ElevatedButtonThemeData(
            style: ElevatedButton.styleFrom(
              backgroundColor: const Color(0xFFEAE6FF),
              elevation: 0,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(22),
              ),
              foregroundColor: const Color(0xFF6A5AAE),
              textStyle: const TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.w600,
              ),
            ),
          ),
          outlinedButtonTheme: OutlinedButtonThemeData(
            style: OutlinedButton.styleFrom(
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(22),
              ),
              textStyle: const TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.w600,
              ),
            ),
          ),
        ),
        initialRoute: Routes.splash,
        routes: Routes.getRoutes(),
      ),
    );
  }
}
