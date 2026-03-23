# VitaGita Flutter (scaffold)

This repository contains a Flutter app scaffold for the VitaGita app with Firebase integration (Authentication + Firestore). It includes pages, widgets, models, and services and is intended to be wired to your Firebase project.

Important notes:

- Do NOT add `assets/images/` or `assets/json/` files here; you will provide them manually.
- You must add platform Firebase configuration files (Android `google-services.json`, iOS `GoogleService-Info.plist`) and enable Authentication + Firestore in the Firebase Console.

Quick start:

1. Install Flutter SDK (stable) and set up platforms.
2. From this project root run:

```powershell
flutter pub get
```

3. Configure Firebase:
   - Create Firebase project.
   - Add Android & iOS apps and download `google-services.json` / `GoogleService-Info.plist` into platform folders.
   - Enable Authentication (Email/Password + Google Sign-In) and Firestore.

4. Run app:

```powershell
flutter run
```

Service overview:
- `lib/services/auth_service.dart` — sign up, login, google sign-in, update profile, delete, logout.
- `lib/services/firestore_service.dart` — shared Firestore helpers.
- `lib/services/shlok_service.dart` — queries for `shloks` collection.
- `lib/services/bookmark_service.dart` — manage bookmarks array on `users/{uid}`.

Firestore structure expected:

users/{uid}:
  firstName
  lastName
  email
  dob
  bookmarks: [shlokId]

shloks/{id}:
  chapter
  number
  title
  summary
  speaker
  theme
  star
  keywords
  sanskrit
  translation
  posterImageUrl

filters/theme/{id}
filters/speaker/{id}
filters/stars/{id}
filters/chapterNumber/{id}
filters/chapter/{id}
