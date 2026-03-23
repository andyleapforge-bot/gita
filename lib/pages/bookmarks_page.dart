import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:firebase_auth/firebase_auth.dart';
import '../theme/colors.dart';
import '../widgets/shlok_card.dart';
import '../widgets/vita_app_bar.dart';
import '../services/bookmark_service.dart';
import '../services/shlok_service.dart';
import '../services/language_service.dart';
import '../services/localization_service.dart';
import '../models/shlok.dart';
import '../routes.dart';

class BookmarksPage extends StatefulWidget {
  @override
  _BookmarksPageState createState() => _BookmarksPageState();
}

class _BookmarksPageState extends State<BookmarksPage> {
  final _bookmarkService = BookmarkService();
  final _shlokService = ShlokService();
  List<Shlok> _bookmarkedShloks = [];

  @override
  void initState() {
    super.initState();
    _load();
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    _load();
  }

  Future<void> _load() async {
    final uid = FirebaseAuth.instance.currentUser?.uid;
    if (uid == null) {
      setState(() => _bookmarkedShloks = []);
      return;
    }
    final langService = Provider.of<LanguageService>(context, listen: false);
    final ids = await _bookmarkService.getUserBookmarks(uid);
    final all =
        await _shlokService.getAllShloks(language: langService.language);
    final map = {for (var s in all) s.id: s};
    setState(() {
      _bookmarkedShloks = ids.map((id) => map[id]).whereType<Shlok>().toList();
    });
  }

  @override
  Widget build(BuildContext context) {
    final langService = Provider.of<LanguageService>(context, listen: true);
    final user = FirebaseAuth.instance.currentUser;
    if (user == null) {
      return Scaffold(
        backgroundColor: AppColors.cream,
        appBar: VitaAppBar(showBackButton: true, showMenu: true),
        body: Center(
          child: Padding(
            padding: const EdgeInsets.all(24),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                Text(
                  LocalizationService.translate('no_bookmarks',
                      langService.language),
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
    return Scaffold(
      backgroundColor: AppColors.cream,
      appBar: VitaAppBar(showBackButton: true, showMenu: true),
      body: _bookmarkedShloks.isEmpty
          ? Center(
              child: Text(
                  LocalizationService.translate(
                      'no_bookmarks', langService.language),
                  style: TextStyle(color: AppColors.summaryText)))
          : ListView.builder(
              padding: EdgeInsets.all(16),
              itemCount: _bookmarkedShloks.length,
              itemBuilder: (_, i) {
                final s = _bookmarkedShloks[i];
                return ShlokCard(
                  shlokId: s.id,
                  chapter: s.chapter,
                  number: s.number,
                  title: s.title,
                  summary: s.summary,
                  poster: s.posterImageUrl,
                  isBookmarked: true,
                  shlok: s,
                  onBookmarkToggled: () async {
                    // After toggle, refresh list
                    await _load();
                  },
                );
              },
            ),
    );
  }
}
