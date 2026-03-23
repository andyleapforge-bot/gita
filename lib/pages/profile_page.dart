import 'package:flutter/material.dart';
import '../routes.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:provider/provider.dart';
import '../theme/colors.dart';
import '../widgets/vita_app_bar.dart';
import '../services/language_service.dart';

class ProfilePage extends StatefulWidget {
  const ProfilePage({Key? key}) : super(key: key);

  @override
  State<ProfilePage> createState() => _ProfilePageState();
}

class _ProfilePageState extends State<ProfilePage> {
  final TextEditingController _nameController = TextEditingController();
  final TextEditingController _dobController = TextEditingController();
  final TextEditingController _emailController = TextEditingController();
  static const double _fieldHeight = 49;

  bool _isEditing = false;
  bool _hasChanges = false;
  String _originalName = '';
  String _originalDob = '';
  String _originalEmail = '';
  String? _editingField; // 'name' | 'dob' | 'email'

  Map<String, dynamic>? _data;

  @override
  void initState() {
    super.initState();
    _load();

    _nameController.addListener(_checkForChanges);
    _dobController.addListener(_checkForChanges);
    _emailController.addListener(_checkForChanges);
  }

  @override
  void dispose() {
    _nameController.dispose();
    _dobController.dispose();
    _emailController.dispose();
    super.dispose();
  }

  void _checkForChanges() {
    setState(() {
      _hasChanges = _nameController.text != _originalName ||
          _dobController.text != _originalDob ||
          _emailController.text != _originalEmail;
    });
  }

  int? _computeAge(String dob) {
    // Expected format: 'DD-Month-YYYY' (e.g., '29-October-2004')
    try {
      final parts = dob.split('-');
      if (parts.length != 3) return null;
      final day = int.tryParse(parts[0]);
      final monthName = parts[1].toLowerCase();
      final year = int.tryParse(parts[2]);
      if (day == null || year == null) return null;
      const months = {
        'january': 1,
        'february': 2,
        'march': 3,
        'april': 4,
        'may': 5,
        'june': 6,
        'july': 7,
        'august': 8,
        'september': 9,
        'october': 10,
        'november': 11,
        'december': 12,
      };
      final month = months[monthName];
      if (month == null) return null;
      final birthDate = DateTime(year, month, day);
      final today = DateTime.now();
      var age = today.year - birthDate.year;
      final beforeBirthdayThisYear = (today.month < birthDate.month) ||
          (today.month == birthDate.month && today.day < birthDate.day);
      if (beforeBirthdayThisYear) age -= 1;
      return age < 0 ? null : age;
    } catch (_) {
      return null;
    }
  }

  Future<void> _load() async {
    final user = FirebaseAuth.instance.currentUser;
    if (user != null) {
      final doc = await FirebaseFirestore.instance
          .collection('users')
          .doc(user.uid)
          .get();

      if (doc.exists) {
        _data = doc.data();
        final firstName = _data?['firstName'] ?? '';
        final lastName = _data?['lastName'] ?? '';
        final fullName = '$firstName $lastName'.trim();

        setState(() {
          _nameController.text = fullName;
          _dobController.text = _data?['dob'] ?? '';
          _emailController.text = _data?['email'] ?? '';

          _originalName = _nameController.text;
          _originalDob = _dobController.text;
          _originalEmail = _emailController.text;
        });
      }
    }
  }

  Future<void> _saveChanges() async {
    final user = FirebaseAuth.instance.currentUser;
    if (user == null) return;

    final nameParts = _nameController.text.trim().split(' ');
    final firstName = nameParts.isNotEmpty ? nameParts[0] : '';
    final lastName = nameParts.length > 1 ? nameParts.sublist(1).join(' ') : '';

    await FirebaseFirestore.instance.collection('users').doc(user.uid).set({
      'firstName': firstName,
      'lastName': lastName,
      'dob': _dobController.text.trim(),
      'email': _emailController.text.trim(),
      'bookmarks': _data?['bookmarks'] ?? [],
    }, SetOptions(merge: true));

    setState(() {
      _originalName = _nameController.text;
      _originalDob = _dobController.text;
      _originalEmail = _emailController.text;
      _hasChanges = false;
    });
  }

  Future<void> _logout() async {
    final langService = Provider.of<LanguageService>(context, listen: false);
    final confirm = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: Text(langService.translate('logout')),
        content: Text(langService.translate('logout_confirm')),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: Text(langService.translate('cancel')),
          ),
          TextButton(
            onPressed: () => Navigator.pop(context, true),
            child: Text(langService.translate('logout')),
          ),
        ],
      ),
    );

    if (confirm == true) {
      await FirebaseAuth.instance.signOut();
      if (mounted) {
        Navigator.of(context).pushReplacementNamed('/login');
      }
    }
  }

  Future<void> _deleteAccount() async {
    final user = FirebaseAuth.instance.currentUser;
    if (user == null) return;

    final langService = Provider.of<LanguageService>(context, listen: false);
    final confirm = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: Text(langService.translate('delete_account')),
        content: Text(langService.translate('delete_confirm')),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: Text(langService.translate('cancel')),
          ),
          TextButton(
            onPressed: () => Navigator.pop(context, true),
            style: TextButton.styleFrom(foregroundColor: Colors.red),
            child: Text(langService.translate('delete')),
          ),
        ],
      ),
    );

    if (confirm == true) {
      await FirebaseFirestore.instance
          .collection('users')
          .doc(user.uid)
          .delete();
      await user.delete();
      if (mounted) {
        Navigator.of(context).pushReplacementNamed('/login');
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final user = FirebaseAuth.instance.currentUser;
    if (user == null) {
      return Scaffold(
        backgroundColor: AppColors.cream,
        appBar: VitaAppBar(showBackButton: true, showMenu: false),
        body: Center(
          child: Padding(
            padding: const EdgeInsets.all(24),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                Text(
                  'Please sign in to view your profile.',
                  style: TextStyle(color: AppColors.summaryText),
                ),
                const SizedBox(height: 12),
                ElevatedButton(
                  onPressed: () =>
                      Navigator.pushNamed(context, Routes.signup),
                  child: const Text('Sign in'),
                ),
              ],
            ),
          ),
        ),
      );
    }
    return WillPopScope(
      onWillPop: () async {
        // From Profile, back should go to Home
        Navigator.pushReplacementNamed(context, Routes.home);
        return false;
      },
      child: Scaffold(
        backgroundColor: AppColors.cream,
        appBar: VitaAppBar(showBackButton: true, showMenu: false),
        body: SingleChildScrollView(
          padding: const EdgeInsets.all(24),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              const Text(
                'Profile',
                style: TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.w700,
                  color: AppColors.titleText,
                ),
              ),
              const SizedBox(height: 10),
              _buildProfileField(
                label: 'Name',
                controller: _nameController,
                fieldKey: 'name',
                placeholder: 'Enter your name',
              ),
              const SizedBox(height: 12),
              _buildProfileField(
                label: 'Date of birth',
                controller: _dobController,
                fieldKey: 'dob',
                placeholder: 'dd/mm/yyyy',
                trailingInfo: _computeAge(_dobController.text) != null
                    ? 'Age: ${_computeAge(_dobController.text)}'
                    : null,
              ),
              const SizedBox(height: 12),
              _buildProfileField(
                label: 'Email',
                controller: _emailController,
                fieldKey: 'email',
                placeholder: 'Enter your email',
              ),
              const SizedBox(height: 18),
              SizedBox(
                width: double.infinity,
                height: 48,
                child: ElevatedButton(
                  onPressed: _logout,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: const Color(0xFFEAE6FF),
                    elevation: 0,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(22),
                    ),
                  ),
                  child: const Text(
                    'Logout',
                    style: TextStyle(
                      color: Color(0xFF6A5AAE),
                      fontWeight: FontWeight.w600,
                      fontSize: 16,
                    ),
                  ),
                ),
              ),
              const SizedBox(height: 10),
              SizedBox(
                width: double.infinity,
                height: 48,
                child: OutlinedButton(
                  onPressed: _deleteAccount,
                  style: OutlinedButton.styleFrom(
                    side: const BorderSide(color: Colors.red),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(22),
                    ),
                  ),
                  child: const Text(
                    'Delete Account',
                    style: TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.w600,
                      color: Colors.red,
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
        bottomNavigationBar: SafeArea(
          top: false,
          child: Container(
            padding: const EdgeInsets.symmetric(vertical: 8),
            color: Colors.transparent,
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: const [
                Text(
                  'गीता सेवक',
                  style: TextStyle(fontWeight: FontWeight.w700),
                ),
                Text(
                  'प्रतीक भारत पलोड़',
                  style: TextStyle(fontWeight: FontWeight.w600),
                ),
                Text('@poet_pratik'),
                Text('+91-7829003200'),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildProfileField({
    required String label,
    required TextEditingController controller,
    required String fieldKey,
    String? trailingInfo,
    String? placeholder,
  }) {
    return Container(
      decoration: BoxDecoration(
        color: AppColors.softYellow,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: AppColors.cardBorder, width: 2),
      ),
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Expanded(
                child: Text(
                  label,
                  style: const TextStyle(
                    fontSize: 14,
                    fontWeight: FontWeight.w600,
                  ),
                ),
              ),
              if (trailingInfo != null)
                Text(
                  trailingInfo,
                  style: TextStyle(
                    fontSize: 12,
                    color: AppColors.titleText.withOpacity(0.7),
                    fontWeight: FontWeight.w500,
                  ),
                ),
            ],
          ),
          const SizedBox(height: 6),
          SizedBox(
            height: _fieldHeight,
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: controller,
                    enabled: _editingField == fieldKey,
                    decoration: InputDecoration(
                      border: InputBorder.none,
                      contentPadding: const EdgeInsets.symmetric(horizontal: 8),
                      hintText: placeholder,
                    ),
                    style: const TextStyle(fontSize: 16),
                  ),
                ),
                IconButton(
                  icon: Icon(
                    _editingField == fieldKey ? Icons.check : Icons.edit,
                    color: AppColors.iconColor,
                  ),
                  onPressed: () {
                    if (_editingField == fieldKey) {
                      if (_hasChanges) {
                        _saveChanges();
                      }
                      setState(() {
                        _editingField = null;
                      });
                    } else {
                      setState(() {
                        _editingField = fieldKey;
                      });
                    }
                  },
                  splashRadius: 20,
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
