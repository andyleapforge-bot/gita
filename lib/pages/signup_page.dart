import 'package:flutter/material.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/services.dart';
import '../theme/colors.dart';
import '../widgets/loading_indicator.dart';
import '../widgets/vita_app_bar.dart';
import '../services/auth_service.dart';
import '../services/firestore_service.dart';
import '../routes.dart';

class SignUpPage extends StatefulWidget {
  @override
  _SignUpPageState createState() => _SignUpPageState();
}

class _SignUpPageState extends State<SignUpPage> {
  final _formKey = GlobalKey<FormState>();
  final _first = TextEditingController();
  final _last = TextEditingController();
  final _email = TextEditingController();
  final _password = TextEditingController();
  final _confirm = TextEditingController();

  static const double _fieldHeight = 52;

  String _day = 'Day';
  String _month = 'Month';
  String _year = 'Year';
  bool _loading = false;
  bool _showPassword = false;
  bool _showConfirmPassword = false;
  static const double _buttonHeight = 48;

  Future<void> _continue() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() => _loading = true);
    try {
      final auth = AuthService();
      final cred =
          await auth.createUser(_email.text.trim(), _password.text.trim());
      final uid = cred.user!.uid;
      final dob = '$_day-$_month-$_year';
      await FirestoreService().setDoc('users', uid, {
        'firstName': _first.text.trim(),
        'lastName': _last.text.trim(),
        'email': _email.text.trim(),
        'dob': dob,
        'bookmarks': [],
      });
      Navigator.pushReplacementNamed(context, Routes.home);
    } catch (e) {
      ScaffoldMessenger.of(context)
          .showSnackBar(SnackBar(content: Text(e.toString())));
    } finally {
      setState(() => _loading = false);
    }
  }

  Future<void> _signInWithApple() async {
    setState(() => _loading = true);
    try {
      final auth = AuthService();
      final cred = await auth.signInWithApple();
      if (cred?.user != null) {
        Navigator.pushReplacementNamed(context, Routes.home);
      }
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
        // From Sign Up, back should exit the app
        SystemNavigator.pop();
        return false;
      },
      child: Scaffold(
        backgroundColor: AppColors.cream,
        appBar: VitaAppBar(showBackButton: false, showMenu: false),
        resizeToAvoidBottomInset: true,
        body: SafeArea(
          child: Center(
            child: SingleChildScrollView(
              padding: EdgeInsets.symmetric(horizontal: 20, vertical: 24),
              child: ConstrainedBox(
                constraints: BoxConstraints(maxWidth: 520),
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: [
                    Align(
                      alignment: Alignment.center,
                      child: Text(
                        'Create account',
                        style: TextStyle(
                          fontSize: 20,
                          color: AppColors.titleText,
                          fontWeight: FontWeight.w700,
                        ),
                      ),
                    ),
                    SizedBox(height: 10),
                    Form(
                      key: _formKey,
                      child: Column(
                        children: [
                          Row(
                            children: [
                              Flexible(
                                fit: FlexFit.loose,
                                child: _buildTextField(_first, 'Name'),
                              ),
                              SizedBox(width: 12),
                              Flexible(
                                fit: FlexFit.loose,
                                child: _buildTextField(_last, 'Last name'),
                              ),
                            ],
                          ),
                          SizedBox(height: 10),
                          _buildDobRow(),
                          SizedBox(height: 10),
                          _buildTextField(_email, 'Email',
                              keyboard: TextInputType.emailAddress),
                          SizedBox(height: 10),
                          _buildPasswordField(
                              _password,
                              'Password',
                              _showPassword,
                              () => setState(
                                  () => _showPassword = !_showPassword)),
                          SizedBox(height: 10),
                          _buildPasswordField(
                              _confirm,
                              'Confirm password',
                              _showConfirmPassword,
                              () => setState(() => _showConfirmPassword =
                                  !_showConfirmPassword)),
                          SizedBox(height: 10),
                          _loading
                              ? LoadingIndicator()
                              : _buildContinueButton(),
                          SizedBox(height: 10),
                          if (!kIsWeb &&
                              (defaultTargetPlatform == TargetPlatform.iOS ||
                                  defaultTargetPlatform ==
                                      TargetPlatform.macOS))
                            SizedBox(
                              width: double.infinity,
                              height: _buttonHeight,
                              child: ElevatedButton.icon(
                                onPressed: _loading ? null : _signInWithApple,
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
                          _buildGoogleButton(),
                          SizedBox(height: 10),
                          Center(
                            child: GestureDetector(
                              onTap: () =>
                                  Navigator.pushNamed(context, Routes.login),
                              child: Text(
                                'Login',
                                style: TextStyle(
                                  fontSize: 16,
                                  color: AppColors.navy,
                                  fontWeight: FontWeight.w600,
                                ),
                              ),
                            ),
                          ),
                          SizedBox(height: 6),
                          Center(
                            child: GestureDetector(
                              onTap: () => Navigator.pushReplacementNamed(
                                  context, Routes.home),
                              child: Text(
                                'Continue as Guest',
                                style: TextStyle(
                                  fontSize: 16,
                                  color: AppColors.navy,
                                  fontWeight: FontWeight.w600,
                                ),
                              ),
                            ),
                          ),
                        ],
                      ),
                    )
                  ],
                ),
              ),
            ),
          ),
        ),
        // bottomNavigationBar removed
      ),
    );
  }

  Widget _buildTextField(TextEditingController c, String hint,
      {TextInputType? keyboard}) {
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
        child: TextFormField(
          controller: c,
          keyboardType: keyboard,
          decoration: InputDecoration(
            border: InputBorder.none,
            hintText: hint,
          ),
          validator: (v) => (v == null || v.trim().isEmpty) ? 'Required' : null,
        ),
      ),
    );
  }

  Widget _buildPasswordField(TextEditingController c, String hint,
      bool showPassword, VoidCallback toggleVisibility) {
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
              child: TextFormField(
                controller: c,
                obscureText: !showPassword,
                decoration: InputDecoration(
                  border: InputBorder.none,
                  hintText: hint,
                  contentPadding: EdgeInsets.symmetric(horizontal: 8),
                ),
                validator: (v) =>
                    (v == null || v.trim().isEmpty) ? 'Required' : null,
              ),
            ),
            IconButton(
              onPressed: toggleVisibility,
              icon: Icon(showPassword ? Icons.visibility_off : Icons.visibility,
                  color: AppColors.iconColor),
              splashRadius: 20,
            )
          ],
        ),
      ),
    );
  }

  Widget _buildDobRow() {
    final days = ['Day', ...List.generate(31, (i) => (i + 1).toString())];
    final months = [
      'Month',
      'January',
      'February',
      'March',
      'April',
      'May',
      'June',
      'July',
      'August',
      'September',
      'October',
      'November',
      'December'
    ];
    final years = [
      'Year',
      ...List.generate(80, (i) => (DateTime.now().year - i).toString())
    ];
    return Row(
      children: [
        Flexible(
            fit: FlexFit.loose,
            child:
                _buildDropdown(days, _day, (v) => setState(() => _day = v!))),
        SizedBox(width: 12),
        Flexible(
            fit: FlexFit.loose,
            child: _buildDropdown(
                months, _month, (v) => setState(() => _month = v!))),
        SizedBox(width: 12),
        Flexible(
            fit: FlexFit.loose,
            child: _buildDropdown(
                years, _year, (v) => setState(() => _year = v!))),
      ],
    );
  }

  Widget _buildDropdown(
      List<String> items, String value, ValueChanged<String?> onChanged) {
    return SizedBox(
      height: _fieldHeight,
      child: Container(
        padding: EdgeInsets.symmetric(horizontal: 16),
        decoration: BoxDecoration(
          color: AppColors.softYellow,
          borderRadius: BorderRadius.circular(12),
          border: Border.all(color: AppColors.cardBorder, width: 2),
        ),
        child: DropdownButton<String>(
          value: value,
          isExpanded: true,
          underline: SizedBox.shrink(),
          dropdownColor: AppColors.softYellow,
          icon: Icon(Icons.arrow_drop_down, color: AppColors.iconColor),
          items: items
              .map((e) => DropdownMenuItem(child: Text(e), value: e))
              .toList(),
          onChanged: onChanged,
        ),
      ),
    );
  }

  Widget _buildContinueButton() {
    return SizedBox(
      width: double.infinity,
      height: 48,
      child: ElevatedButton(
        onPressed: _continue,
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
    );
  }

  Widget _buildGoogleButton() {
    return SizedBox(
      width: double.infinity,
      height: 48,
      child: ElevatedButton(
        onPressed: () async {
          setState(() => _loading = true);
          try {
            final auth = AuthService();
            final cred = await auth.signInWithGoogleIfExistingUser();
            if (cred != null) {
              Navigator.pushReplacementNamed(context, Routes.home);
            } else {
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(
                    content: Text('Account not found. Please sign up first.')),
              );
            }
          } finally {
            setState(() => _loading = false);
          }
        },
        style: ElevatedButton.styleFrom(
          backgroundColor: Color(0xFFEAE6FF),
          elevation: 0,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(22),
          ),
        ),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.g_mobiledata, color: Color(0xFF6A5AAE), size: 24),
            SizedBox(width: 4),
            Text(
              'Continue with Google',
              style: TextStyle(
                fontSize: 16,
                color: Color(0xFF6A5AAE),
                fontWeight: FontWeight.w600,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
