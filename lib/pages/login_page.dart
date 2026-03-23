import 'package:flutter/material.dart';
import 'package:flutter/foundation.dart';
import '../routes.dart';
import '../theme/colors.dart';
import '../services/auth_service.dart';
import '../routes.dart';
import '../widgets/loading_indicator.dart';
import '../widgets/vita_app_bar.dart';

class LoginPage extends StatefulWidget {
  @override
  _LoginPageState createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final _email = TextEditingController();
  final _password = TextEditingController();
  bool _loading = false;
  bool _showPassword = false;
  static const double _fieldHeight = 52;
  static const double _buttonHeight = 48;

  Future<void> _login() async {
    setState(() => _loading = true);
    try {
      await AuthService().login(_email.text.trim(), _password.text.trim());
      Navigator.pushReplacementNamed(context, Routes.home);
    } catch (e) {
      ScaffoldMessenger.of(context)
          .showSnackBar(SnackBar(content: Text(e.toString())));
    } finally {
      setState(() => _loading = false);
    }
  }

  Future<void> _loginWithApple() async {
    setState(() => _loading = true);
    try {
      await AuthService().signInWithApple();
      Navigator.pushReplacementNamed(context, Routes.home);
    } catch (e) {
      ScaffoldMessenger.of(context)
          .showSnackBar(SnackBar(content: Text(e.toString())));
    } finally {
      setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return WillPopScope(
      onWillPop: () async {
        // From Login, back should go to Sign Up
        Navigator.pushReplacementNamed(context, Routes.signup);
        return false;
      },
      child: Scaffold(
        backgroundColor: AppColors.cream,
        appBar: VitaAppBar(showBackButton: false, showMenu: false),
        body: SafeArea(
          child: Stack(
            children: [
              // Centered content
              Center(
                child: SingleChildScrollView(
                  padding: EdgeInsets.symmetric(horizontal: 20, vertical: 24),
                  child: ConstrainedBox(
                    constraints: BoxConstraints(maxWidth: 520),
                    child: Column(
                      mainAxisSize: MainAxisSize.min,
                      crossAxisAlignment: CrossAxisAlignment.stretch,
                      children: [
                        SizedBox(height: 8),
                        Align(
                          alignment: Alignment.center,
                          child: Text(
                            'Login in your account',
                            style: TextStyle(
                              fontSize: 20,
                              fontWeight: FontWeight.w700,
                              color: AppColors.titleText,
                            ),
                          ),
                        ),
                        SizedBox(height: 20),
                        _buildField(
                          controller: _email,
                          hint: 'Enter your email',
                          keyboard: TextInputType.emailAddress,
                        ),
                        SizedBox(height: 12),
                        _buildPasswordField(
                          controller: _password,
                          hint: 'Enter your password',
                        ),
                        SizedBox(height: 18),
                        _loading
                            ? LoadingIndicator()
                            : SizedBox(
                                width: double.infinity,
                                height: _buttonHeight,
                                child: ElevatedButton(
                                  onPressed: _login,
                                  style: ElevatedButton.styleFrom(
                                    backgroundColor: Color(0xFFEAE6FF),
                                    elevation: 0,
                                    shape: RoundedRectangleBorder(
                                      borderRadius: BorderRadius.circular(22),
                                    ),
                                  ),
                                  child: Text(
                                    'Continue',
                                    style: TextStyle(
                                      color: Color(0xFF6A5AAE),
                                      fontWeight: FontWeight.w600,
                                      fontSize: 16,
                                    ),
                                  ),
                                ),
                              ),
                        SizedBox(height: 10),
                        if (!kIsWeb &&
                            (defaultTargetPlatform == TargetPlatform.iOS ||
                                defaultTargetPlatform == TargetPlatform.macOS))
                          SizedBox(
                            width: double.infinity,
                            height: _buttonHeight,
                            child: ElevatedButton.icon(
                              onPressed: _loading ? null : _loginWithApple,
                              icon: Icon(Icons.apple, color: Colors.white),
                              label: Text(
                                'Sign in with Apple',
                                style: TextStyle(
                                  color: Colors.white,
                                  fontWeight: FontWeight.w600,
                                  fontSize: 16,
                                ),
                              ),
                              style: ElevatedButton.styleFrom(
                                backgroundColor: Colors.black,
                                elevation: 0,
                                shape: RoundedRectangleBorder(
                                  borderRadius: BorderRadius.circular(22),
                                ),
                              ),
                            ),
                          ),
                        SizedBox(height: 10),
                        Center(
                          child: TextButton(
                            onPressed: () =>
                                Navigator.pushNamed(context, Routes.signup),
                            child: Text('Go to Sign Up',
                                style: TextStyle(color: AppColors.navy)),
                          ),
                        ),
                        Center(
                          child: TextButton(
                            onPressed: () =>
                                Navigator.pushReplacementNamed(context, Routes.home),
                            child: Text('Continue as Guest',
                                style: TextStyle(color: AppColors.navy)),
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildField({
    required TextEditingController controller,
    required String hint,
    TextInputType? keyboard,
  }) {
    return SizedBox(
      height: _fieldHeight,
      child: Container(
        decoration: BoxDecoration(
          color: AppColors.softYellow,
          borderRadius: BorderRadius.circular(12),
          border: Border.all(color: AppColors.cardBorder, width: 2),
        ),
        padding: EdgeInsets.symmetric(horizontal: 16),
        alignment: Alignment.center,
        child: TextField(
          controller: controller,
          keyboardType: keyboard,
          decoration: InputDecoration(
            border: InputBorder.none,
            hintText: hint,
          ),
        ),
      ),
    );
  }

  Widget _buildPasswordField({
    required TextEditingController controller,
    required String hint,
  }) {
    return SizedBox(
      height: _fieldHeight,
      child: Container(
        decoration: BoxDecoration(
          color: AppColors.softYellow,
          borderRadius: BorderRadius.circular(12),
          border: Border.all(color: AppColors.cardBorder, width: 2),
        ),
        padding: EdgeInsets.symmetric(horizontal: 8),
        child: Row(
          children: [
            Expanded(
              child: TextField(
                controller: controller,
                obscureText: !_showPassword,
                decoration: InputDecoration(
                  border: InputBorder.none,
                  hintText: hint,
                  contentPadding: EdgeInsets.symmetric(horizontal: 8),
                ),
              ),
            ),
            IconButton(
              onPressed: () => setState(() => _showPassword = !_showPassword),
              icon: Icon(
                  _showPassword ? Icons.visibility_off : Icons.visibility,
                  color: AppColors.iconColor),
              splashRadius: 20,
            )
          ],
        ),
      ),
    );
  }
}
