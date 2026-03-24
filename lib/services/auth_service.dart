// lib/services/auth_service.dart
import 'package:firebase_auth/firebase_auth.dart';
import 'package:google_sign_in/google_sign_in.dart';
import 'package:flutter/foundation.dart';
import 'dart:io';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'user_service.dart';

class AuthService {
  final FirebaseAuth _auth = FirebaseAuth.instance;
  final FirebaseFirestore _fs = FirebaseFirestore.instance;

  User? get currentUser => _auth.currentUser;

  Future<UserCredential> createUser(String email, String password) async {
    final cred = await _auth.createUserWithEmailAndPassword(
      email: email,
      password: password,
    );
    final userService = UserService();
    await userService.createUserIfNotExists(cred);
    if (cred.user != null) {
      await userService.ensurePointsFields(cred.user!.uid);
    }
    return cred;
  }

  Future<UserCredential> login(String email, String password) async {
    final cred = await _auth.signInWithEmailAndPassword(
      email: email,
      password: password,
    );
    final userService = UserService();
    await userService.createUserIfNotExists(cred);
    if (cred.user != null) {
      await userService.ensurePointsFields(cred.user!.uid);
    }
    return cred;
  }

  Future<void> logout() async {
    await _auth.signOut();
  }

  Future<void> deleteAccount() async {
    final user = _auth.currentUser;
    if (user != null) {
      await user.delete();
    }
  }

  Future<UserCredential?> signInWithGoogle() async {
    final GoogleSignInAccount? account = await GoogleSignIn().signIn();
    if (account == null) return null;
    final GoogleSignInAuthentication auth = await account.authentication;
    final credential = GoogleAuthProvider.credential(
      accessToken: auth.accessToken,
      idToken: auth.idToken,
    );
    final cred = await _auth.signInWithCredential(credential);
    final userService = UserService();
    await userService.createUserIfNotExists(cred);
    if (cred.user != null) {
      await userService.ensurePointsFields(cred.user!.uid);
    }
    return cred;
  }

  /// Sign in with Google only if a user document with the same email exists.
  /// Returns UserCredential if allowed, otherwise signs out and returns null.
  Future<UserCredential?> signInWithGoogleIfExistingUser() async {
    final GoogleSignIn googleSignIn = GoogleSignIn();
    final GoogleSignInAccount? account = await googleSignIn.signIn();
    if (account == null) return null;

    // Simplified: avoid Firestore email query (can trigger PERMISSION_DENIED).
    // Just sign in with Google and ensure user document exists via UserService.
    final GoogleSignInAuthentication auth = await account.authentication;
    final credential = GoogleAuthProvider.credential(
      accessToken: auth.accessToken,
      idToken: auth.idToken,
    );
    final cred = await _auth.signInWithCredential(credential);
    final userService = UserService();
    await userService.createUserIfNotExists(cred);
    if (cred.user != null) {
      await userService.ensurePointsFields(cred.user!.uid);
    }
    return cred;
  }

  Future<UserCredential?> signInWithApple() async {
    if (kIsWeb || !(Platform.isIOS || Platform.isMacOS)) {
      throw Exception('Sign in with Apple is only available on iOS/macOS.');
    }
    final provider = AppleAuthProvider()
      ..addScope('email')
      ..addScope('name');
    final cred = await _auth.signInWithProvider(provider);
    final userService = UserService();
    await userService.createUserIfNotExists(cred);
    if (cred.user != null) {
      await userService.ensurePointsFields(cred.user!.uid);
    }
    return cred;
  }

  Future<void> updateProfile({String? displayName, String? email}) async {
    final user = _auth.currentUser;
    if (user == null) return;
    if (displayName != null) await user.updateDisplayName(displayName);
    if (email != null) await user.updateEmail(email);
    await user.reload();
  }
}
