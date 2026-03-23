// Generated manually from ios/Runner/GoogleService-Info.plist.
// If you later run `flutterfire configure`, replace this file.

import 'package:firebase_core/firebase_core.dart';
import 'package:flutter/foundation.dart';

class DefaultFirebaseOptions {
  static FirebaseOptions get currentPlatform {
    if (kIsWeb) {
      throw UnsupportedError(
        'DefaultFirebaseOptions are not supported for web.',
      );
    }

    switch (defaultTargetPlatform) {
      case TargetPlatform.iOS:
        return ios;
      case TargetPlatform.macOS:
        return ios;
      case TargetPlatform.android:
      case TargetPlatform.fuchsia:
      case TargetPlatform.linux:
      case TargetPlatform.windows:
        throw UnsupportedError(
          'DefaultFirebaseOptions are not configured for this platform.',
        );
    }
  }

  static const FirebaseOptions ios = FirebaseOptions(
    apiKey: 'AIzaSyCKH76BTsGHVDEojsp_4DxKCq4dddmYuV0',
    appId: '1:1067642694608:ios:112e71fed1700622fc27d5',
    messagingSenderId: '1067642694608',
    projectId: 'vitagita-3c6af',
    storageBucket: 'vitagita-3c6af.firebasestorage.app',
    iosBundleId: 'com.example.vitagita',
    iosClientId:
        '1067642694608-cjmn9k4fht2790qn9p5c3mm14cimknst.apps.googleusercontent.com',
  );
}
