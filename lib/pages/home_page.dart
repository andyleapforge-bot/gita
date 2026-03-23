// lib/pages/home_page.dart
import 'package:flutter/material.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/services.dart';
import 'package:provider/provider.dart';
import '../theme/colors.dart';
import '../widgets/search_bar.dart';
import '../widgets/shlok_card.dart';
import '../widgets/filter_chip_widget.dart';
import '../widgets/vita_app_bar.dart';
import '../services/shlok_service.dart';
import '../services/user_service.dart';
import '../services/language_service.dart';
import '../services/point_event_bus.dart';
import '../routes.dart';
import '../models/shlok.dart';
import '../services/localization_service.dart';

class HomePage extends StatefulWidget {
  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final ShlokService _shlokService = ShlokService();
  final UserService _userService = UserService();
  List<Shlok> items = [];
  String _search = '';
  Set<String> _userBookmarks = {};
  String? _selectedTheme;
  String? _selectedSpeaker;
  Set<int> _selectedStars = {};
  Set<int> _selectedChapterNumbers = {};
  Set<int> _selectedChapters = {};

  @override
  void initState() {
    super.initState();
    _load();
    _updateStreak();
  }

  Future<void> _updateStreak() async {
    final uid = FirebaseAuth.instance.currentUser?.uid;
    if (uid != null) {
      try {
        await _userService.updateStreak(uid);
      } catch (e) {
        // Silently fail if streak update fails
      }
    }
  }

  Future<void> _onSearchChanged(String v) async {
    setState(() => _search = v);
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    // Reload shloks when language changes
    final langService = Provider.of<LanguageService>(context, listen: true);
    _load();
  }

  Future<void> _load() async {
    final langService = Provider.of<LanguageService>(context, listen: false);
    final all =
        await _shlokService.getAllShloks(language: langService.language);
    String? uid = FirebaseAuth.instance.currentUser?.uid;
    if (uid != null) {
      try {
        await _userService.ensurePointsFields(uid);
        final list = await _userService.getBookmarks(uid);
        _userBookmarks = list.toSet();
      } catch (_) {
        _userBookmarks = {};
      }
    } else {
      _userBookmarks = {};
    }
    setState(() => items = all);
  }

  List<Shlok> _applySearch() {
    List<Shlok> res = items;
    if (_search.isNotEmpty) {
      final q = _search.toLowerCase();
      res = res.where((s) {
        return s.title.toLowerCase().contains(q) ||
            s.summary.toLowerCase().contains(q) ||
            s.keywords.any((k) => k.toLowerCase().contains(q));
      }).toList();
    }
    if (_selectedTheme != null) {
      res = res.where((s) => s.theme == _selectedTheme).toList();
    }
    if (_selectedSpeaker != null) {
      res = res.where((s) => s.speaker == _selectedSpeaker).toList();
    }
    if (_selectedStars.isNotEmpty) {
      res = res.where((s) => _selectedStars.contains(s.star)).toList();
    }
    if (_selectedChapterNumbers.isNotEmpty) {
      res = res
          .where((s) => _selectedChapterNumbers.contains(s.number.floor()))
          .toList();
    }
    if (_selectedChapters.isNotEmpty) {
      res = res.where((s) => _selectedChapters.contains(s.chapter)).toList();
    }
    return res;
  }

  List<Shlok> _itemsForFilter(String type) {
    List<Shlok> res = items;
    if (_search.isNotEmpty) {
      final q = _search.toLowerCase();
      res = res.where((s) {
        return s.title.toLowerCase().contains(q) ||
            s.summary.toLowerCase().contains(q) ||
            s.keywords.any((k) => k.toLowerCase().contains(q));
      }).toList();
    }
    if (type != 'Theme' && _selectedTheme != null) {
      res = res.where((s) => s.theme == _selectedTheme).toList();
    }
    if (type != 'Speaker' && _selectedSpeaker != null) {
      res = res.where((s) => s.speaker == _selectedSpeaker).toList();
    }
    if (type != 'Stars' && _selectedStars.isNotEmpty) {
      res = res.where((s) => _selectedStars.contains(s.star)).toList();
    }
    if (type != 'Shlok Number' && _selectedChapterNumbers.isNotEmpty) {
      res = res
          .where((s) => _selectedChapterNumbers.contains(s.number.floor()))
          .toList();
    }
    if (type != 'Chapter' && _selectedChapters.isNotEmpty) {
      res = res.where((s) => _selectedChapters.contains(s.chapter)).toList();
    }
    return res;
  }

  void _openFilter(String type) {
    final base = _itemsForFilter(type);
    List<String> options = [];
    final lang = Provider.of<LanguageService>(context, listen: false).language;
    if (type == 'Theme') {
      options = base.map((e) => e.theme).toSet().toList()..sort();
    } else if (type == 'Speaker') {
      options = base.map((e) => e.speaker).toSet().toList()..sort();
    } else if (type == 'Chapter') {
      options = base.map((e) => e.chapter.toString()).toSet().toList()
        ..sort((a, b) => int.parse(a).compareTo(int.parse(b)));
    } else if (type == 'Shlok Number') {
      options = base.map((e) => e.number.floor().toString()).toSet().toList()
        ..sort((a, b) => int.parse(a).compareTo(int.parse(b)));
    } else if (type == 'Stars') {
      options = base.map((e) => e.star.toString()).toSet().toList()
        ..sort((a, b) => int.parse(a).compareTo(int.parse(b)));
    }

    String displayOpt(String opt) {
      if (lang != 'hi') return opt;
      if (type == 'Speaker') {
        const speakerMap = {
          'Arjun': 'अर्जुन',
          'Arjuna': 'अर्जुन',
          'Krishn': 'कृष्ण',
          'Krishna': 'कृष्ण',
          'Sanjay': 'संजय',
          'Bhishma': 'भीष्म',
          'Bhisma': 'भीष्म',
          'Karna': 'कर्ण',
          'Duryodhan': 'दुर्योधन',
          'Duryodhana': 'दुर्योधन',
          'Dhritarashtra': 'धृतराष्ट्र',
          'Dhritrashtra': 'धृतराष्ट्र',
          'Vyas': 'व्यास',
          'Vyasa': 'व्यास',
          'Narayan': 'नारायण',
          'Narayana': 'नारायण',
          'Indra': 'इन्द्र',
          'Yudhishthir': 'युधिष्ठिर',
          'Yudhishthira': 'युधिष्ठिर',
          'Brahma': 'ब्रह्मा',
          'Shiva': 'शिव',
          'Mahadev': 'महादेव',
        };
        return speakerMap[opt] ?? opt;
      }
      if (type == 'Theme') {
        const themeMap = {
          'Strategy': 'रणनीति',
          'Duty': 'कर्तव्य',
          'Devotion': 'भक्ति',
          'Knowledge': 'ज्ञान',
          'Self': 'स्व',
          'Renunciation': 'संन्यास',
          'Meditation': 'ध्यान',
          'Action': 'कर्म',
          'Practice': 'अभ्यास',
          'Wisdom': 'प्रज्ञा',
          'Faith': 'श्रद्धा',
          'Nature': 'स्वभाव',
          // Additional themes from data showing in English
          'Attachment': 'आसक्ति',
          'Attributes': 'गुण',
          'Creation': 'सृष्टि',
          'Decision': 'निर्णय',
          'Delusion': 'मोह',
          'Desires': 'इच्छाएं',
          'Destiny': 'भाग्य',
          'Determine': 'दृढ़ निश्चय',
          'Dharm': 'धर्म',
          'Discipline': 'अनुशासन',
          'Karma': 'कर्म',
        };
        return themeMap[opt] ?? opt;
      }
      if (type == 'Stars' || type == 'Chapter' || type == 'Shlok Number') {
        const digitMap = {
          '0': '०',
          '1': '१',
          '2': '२',
          '3': '३',
          '4': '४',
          '5': '५',
          '6': '६',
          '7': '७',
          '8': '८',
          '9': '९',
        };
        return opt.split('').map((c) => digitMap[c] ?? c).join();
      }
      return opt;
    }

    showModalBottomSheet(
      context: context,
      backgroundColor: Colors.white,
      isScrollControlled: true,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(16)),
      ),
      builder: (_) {
        return StatefulBuilder(
          builder: (ctx, setSheetState) {
            void toggleOption(bool newVal, String opt) {
              setSheetState(() {});
              setState(() {
                if (type == 'Theme') {
                  _selectedTheme = newVal ? opt : null;
                } else if (type == 'Speaker') {
                  _selectedSpeaker = newVal ? opt : null;
                } else if (type == 'Chapter') {
                  final val = int.tryParse(opt);
                  if (val != null) {
                    if (newVal) {
                      _selectedChapters.add(val);
                    } else {
                      _selectedChapters.remove(val);
                    }
                  }
                } else if (type == 'Shlok Number') {
                  final val = int.tryParse(opt);
                  if (val != null) {
                    if (newVal) {
                      _selectedChapterNumbers.add(val);
                    } else {
                      _selectedChapterNumbers.remove(val);
                    }
                  }
                } else if (type == 'Stars') {
                  final val = int.tryParse(opt);
                  if (val != null) {
                    if (newVal) {
                      _selectedStars.add(val);
                    } else {
                      _selectedStars.remove(val);
                    }
                  }
                }
              });
            }

            return Padding(
              padding: const EdgeInsets.fromLTRB(16, 16, 16, 24),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(
                          LocalizationService.translate(
                              type == 'Stars'
                                  ? 'filter_by_star'
                                  : type == 'Theme'
                                      ? 'filter_by_theme'
                                      : type == 'Speaker'
                                          ? 'filter_by_speaker'
                                          : type == 'Chapter'
                                              ? 'filter_by_chapter'
                                              : 'filter_by_shlok_number',
                              Provider.of<LanguageService>(context,
                                      listen: false)
                                  .language),
                          style: TextStyle(
                              fontSize: 16, fontWeight: FontWeight.w600)),
                      TextButton(
                        onPressed: () {
                          setState(() {
                            if (type == 'Theme') _selectedTheme = null;
                            if (type == 'Speaker') _selectedSpeaker = null;
                            if (type == 'Stars') _selectedStars.clear();
                            if (type == 'Shlok Number')
                              _selectedChapterNumbers.clear();
                            if (type == 'Chapter') _selectedChapters.clear();
                          });
                          Navigator.pop(context);
                        },
                        child: Text(LocalizationService.translate(
                            'clear',
                            Provider.of<LanguageService>(context, listen: false)
                                .language)),
                      )
                    ],
                  ),
                  SizedBox(height: 8),
                  Flexible(
                    child: ListView.builder(
                      shrinkWrap: true,
                      itemCount: options.length,
                      itemBuilder: (_, i) {
                        final opt = options[i];
                        final display = displayOpt(opt);
                        bool checked = false;
                        if (type == 'Theme') checked = _selectedTheme == opt;
                        if (type == 'Speaker')
                          checked = _selectedSpeaker == opt;
                        if (type == 'Chapter')
                          checked =
                              _selectedChapters.contains(int.tryParse(opt));
                        if (type == 'Shlok Number')
                          checked = _selectedChapterNumbers
                              .contains(int.tryParse(opt));
                        if (type == 'Stars')
                          checked = _selectedStars.contains(int.tryParse(opt));
                        return ListTile(
                          title: Text(display),
                          trailing: Checkbox(
                            value: checked,
                            onChanged: (v) {
                              toggleOption(v == true, opt);
                            },
                            activeColor: AppColors.gold,
                            checkColor: Colors.white,
                          ),
                          onTap: () {
                            // Toggle via tapping the whole tile as well
                            final isChecked = checked;
                            final newVal = !isChecked;
                            toggleOption(newVal, opt);
                          },
                        );
                      },
                    ),
                  ),
                  SizedBox(height: 12),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.end,
                    children: [
                      TextButton(
                          onPressed: () => Navigator.pop(context),
                          child: Text(LocalizationService.translate(
                              'cancel',
                              Provider.of<LanguageService>(context,
                                      listen: false)
                                  .language))),
                      SizedBox(width: 12),
                      ElevatedButton(
                          onPressed: () => Navigator.pop(context),
                          child: Text(LocalizationService.translate(
                              'apply',
                              Provider.of<LanguageService>(context,
                                      listen: false)
                                  .language))),
                    ],
                  )
                ],
              ),
            );
          },
        );
      },
    );
  }

  Widget _buildFilterChips() {
    final langService = Provider.of<LanguageService>(context, listen: true);
    return Column(
      children: [
        Row(
          children: [
            Expanded(
                child: FilterChipWidget(
                    label: langService.translate('theme'),
                    selected: _selectedTheme != null,
                    onTap: () => _openFilter('Theme'))),
            SizedBox(width: 12),
            Expanded(
                child: FilterChipWidget(
                    label: langService.translate('speaker'),
                    selected: _selectedSpeaker != null,
                    onTap: () => _openFilter('Speaker'))),
            SizedBox(width: 12),
            Expanded(
                child: FilterChipWidget(
                    label: langService.translate('stars'),
                    selected: _selectedStars.isNotEmpty,
                    onTap: () => _openFilter('Stars'))),
          ],
        ),
        SizedBox(height: 12),
        Row(
          children: [
            Expanded(
                child: FilterChipWidget(
                    label: langService.translate('chapter'),
                    selected: _selectedChapters.isNotEmpty,
                    onTap: () => _openFilter('Chapter'))),
            SizedBox(width: 12),
            Expanded(
                child: FilterChipWidget(
                    label: langService.translate('shlok_number'),
                    selected: _selectedChapterNumbers.isNotEmpty,
                    onTap: () => _openFilter('Shlok Number'))),
          ],
        ),
      ],
    );
  }

  @override
  Widget build(BuildContext context) {
    final visibleItems = _applySearch();
    final langService = Provider.of<LanguageService>(context);

    return WillPopScope(
      onWillPop: () async {
        SystemNavigator.pop();
        return false;
      },
      child: Scaffold(
        backgroundColor: AppColors.cream,
        appBar:
            VitaAppBar(showBackButton: false, showMenu: true, showStreak: true),
        body: Padding(
          padding: EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              VitaSearchBar(onChanged: _onSearchChanged),
              SizedBox(height: 16),
              _buildFilterChips(),
              SizedBox(height: 16),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                    langService.language == 'hi'
                        ? '${visibleItems.length} परिणाम दिखा रहे हैं'
                        : 'Showing ${visibleItems.length} results',
                    style: TextStyle(
                      color: AppColors.resultText,
                      fontSize: 14,
                      fontWeight: FontWeight.w500,
                    ),
                  ),
                  GestureDetector(
                    onTap: () {
                      setState(() {
                        _selectedTheme = null;
                        _selectedSpeaker = null;
                        _selectedStars.clear();
                        _selectedChapterNumbers.clear();
                        _selectedChapters.clear();
                      });
                    },
                    child: Text(
                      langService.translate('clear_filters'),
                      style: TextStyle(
                        color: AppColors.clearFiltersText,
                        fontSize: 14,
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                  ),
                ],
              ),
              SizedBox(height: 16),
              Expanded(
                child: visibleItems.isEmpty
                    ? Center(
                        child: Text(
                          langService.translate('no_shloks'),
                          style: TextStyle(color: AppColors.summaryText),
                        ),
                      )
                    : ListView.builder(
                        itemCount: visibleItems.length,
                        itemBuilder: (_, i) {
                          final shlok = visibleItems[i];
                          final isBm = _userBookmarks.contains(shlok.id);
                          return ShlokCard(
                            shlokId: shlok.id,
                            chapter: shlok.chapter,
                            number: shlok.number,
                            title: shlok.title,
                            summary: shlok.summary,
                            poster: shlok.posterImageUrl,
                            isBookmarked: isBm,
                            shlok: shlok,
                            searchQuery: _search.isNotEmpty ? _search : null,
                            onBookmarkToggled: () async {
                              // Optimistic UI: flip local state immediately
                              final uid =
                                  FirebaseAuth.instance.currentUser?.uid;
                              final wasBookmarked =
                                  _userBookmarks.contains(shlok.id);
                              setState(() {
                                if (wasBookmarked) {
                                  _userBookmarks.remove(shlok.id);
                                } else {
                                  _userBookmarks.add(shlok.id);
                                }
                              });

                              if (uid != null) {
                                try {
                                  if (wasBookmarked) {
                                    await _userService.removeBookmark(
                                        uid, shlok.id);
                                  } else {
                                    await _userService.addBookmark(
                                        uid, shlok.id);
                                  }
                                  // Refresh bookmarks from backend after toggle
                                  final list =
                                      await _userService.getBookmarks(uid);
                                  setState(() {
                                    _userBookmarks = list.toSet();
                                  });
                                } catch (_) {
                                  // revert optimistic change on failure
                                  setState(() {
                                    if (wasBookmarked) {
                                      _userBookmarks.add(shlok.id);
                                    } else {
                                      _userBookmarks.remove(shlok.id);
                                    }
                                  });
                                  ScaffoldMessenger.of(context).showSnackBar(
                                    SnackBar(
                                        content: Text(
                                            'Could not update bookmark. It will sync when online.')),
                                  );
                                }
                              } else {
                                // not logged in
                                ScaffoldMessenger.of(context).showSnackBar(
                                  SnackBar(
                                      content: Text(
                                          'Please log in to save bookmarks')),
                                );
                                // revert optimistic change
                                setState(() {
                                  if (wasBookmarked) {
                                    _userBookmarks.add(shlok.id);
                                  } else {
                                    _userBookmarks.remove(shlok.id);
                                  }
                                });
                              }
                            },
                          );
                        },
                      ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
