import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import '../theme/colors.dart';
import '../widgets/vita_app_bar.dart';
import '../services/language_service.dart';
import '../services/localization_service.dart';
import '../services/user_service.dart';
import '../services/point_event_bus.dart';

class GamificationPage extends StatefulWidget {
  const GamificationPage({super.key});

  @override
  State<GamificationPage> createState() => _GamificationPageState();
}

class _GamificationPageState extends State<GamificationPage> {
  final _userService = UserService();
  String? _uid;
  int _localPoints = 0; // Local optimistic state

  @override
  void initState() {
    super.initState();
    _uid = FirebaseAuth.instance.currentUser?.uid;
  }

  @override
  void dispose() {
    super.dispose();
  }

  String _digits(String value, String lang) {
    if (lang != 'hi') return value;
    const map = {
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
    return value.split('').map((c) => map[c] ?? c).join();
  }

  /// Determine user level based on cumulative points
  String _getLevelKey(int points) {
    if (points <= 500) return 'level_shishu';
    if (points <= 2000) return 'level_sainik';
    if (points <= 5000) return 'level_rathi';
    if (points <= 20000) return 'level_atirathi';
    return 'level_maharathi';
  }

  @override
  Widget build(BuildContext context) {
    return Consumer<LanguageService>(builder: (context, langService, _) {
      final lang = langService.language;
      final t = (String key) => LocalizationService.translate(key, lang);

      final activities = [
        {'name': t('activity_login'), 'points': '5'},
        {'name': t('activity_search'), 'points': '10'},
        {'name': t('activity_listen'), 'points': '20'},
        {'name': t('activity_share'), 'points': '50'},
      ];

      final levels = [
        {'range': '0-500', 'level': t('level_shishu'), 'image': 'shishu_new'},
        {
          'range': '501-2000',
          'level': t('level_sainik'),
          'image': 'sainik_zoom'
        },
        {'range': '2001-5000', 'level': t('level_rathi'), 'image': 'rathi_new'},
        {'range': '5001-20000', 'level': t('level_atirathi'), 'image': 'ath'},
        {
          'range': '>20001',
          'level': t('level_maharathi'),
          'image': 'maharati_new'
        },
      ];

      return Scaffold(
        backgroundColor: AppColors.backgroundBeige,
        appBar: VitaAppBar(showBackButton: true, showMenu: true),
        body: ListView(
          padding: const EdgeInsets.all(16),
          children: [
            _buildCard(
              titleLeft: t('activity_header'),
              titleRight: t('points_header'),
              rows: activities
                  .map((row) => _RowData(
                        left: row['name']!,
                        right: _digits(row['points']!, lang),
                      ))
                  .toList(),
            ),
            const SizedBox(height: 16),
            _buildCard(
              titleLeft: t('cumulative_points'),
              titleRight: t('level'),
              rows: levels
                  .map((row) => _RowData(
                        left: _digits(row['range']!, lang),
                        right: row['level']!,
                        imageName: row['image'] as String?,
                      ))
                  .toList(),
            ),
            const SizedBox(height: 16),
            _uid == null
                ? _buildPointsCard(
                    title: t('your_points'),
                    value: _digits('0', lang),
                    levelKey: null,
                    lang: lang,
                  )
                : StreamBuilder<DocumentSnapshot<Map<String, dynamic>>>(
                    stream: FirebaseFirestore.instance
                        .collection(UserService.usersCollection)
                        .doc(_uid)
                        .snapshots(),
                    builder: (context, snapshot) {
                      final loading =
                          snapshot.connectionState == ConnectionState.waiting;
                      int firebasePoints = 0;
                      if (snapshot.hasData && snapshot.data?.data() != null) {
                        final data = snapshot.data!.data()!;
                        final val = data['rewardScore'] ?? data['points'];
                        if (val is int)
                          firebasePoints = val;
                        else if (val is num) firebasePoints = val.toInt();
                      }

                      // Listen to EventBus for optimistic updates
                      return StreamBuilder<int>(
                        stream: PointEventBus().pointsStream,
                        builder: (context, eventSnapshot) {
                          int displayPoints = firebasePoints;

                          // If optimistic event received, add to Firestore points
                          if (eventSnapshot.hasData) {
                            displayPoints += eventSnapshot.data!;
                          }

                          final display = _digits(
                            loading ? '...' : displayPoints.toString(),
                            lang,
                          );
                          final levelKey = _getLevelKey(displayPoints);
                          return _buildPointsCard(
                            title: t('your_points'),
                            value: display,
                            levelKey: levelKey,
                            lang: lang,
                          );
                        },
                      );
                    },
                  ),
          ],
        ),
      );
    });
  }

  Widget _buildCard(
      {required String titleLeft,
      required String titleRight,
      required List<_RowData> rows}) {
    return Card(
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
        side: const BorderSide(color: AppColors.cardBorder, width: 1),
      ),
      elevation: 0,
      color: AppColors.cardBackground,
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Expanded(
                  child: Text(
                    titleLeft,
                    style: const TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.w700,
                      color: AppColors.titleText,
                    ),
                  ),
                ),
                Text(
                  titleRight,
                  style: const TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.w700,
                    color: AppColors.titleText,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 8),
            const Divider(height: 1, color: AppColors.cardBorder),
            const SizedBox(height: 8),
            ...rows.map((row) => Padding(
                  padding: const EdgeInsets.symmetric(vertical: 8),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Expanded(
                        child: Text(
                          row.left,
                          style: const TextStyle(
                            fontSize: 14,
                            fontWeight: FontWeight.w500,
                            color: AppColors.summaryText,
                          ),
                        ),
                      ),
                      Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Container(
                            padding: const EdgeInsets.symmetric(
                                horizontal: 12, vertical: 6),
                            decoration: BoxDecoration(
                              color: AppColors.badgeBackground.withOpacity(0.1),
                              borderRadius: BorderRadius.circular(8),
                              border: Border.all(
                                color: AppColors.cardBorder,
                                width: 1,
                              ),
                            ),
                            constraints: const BoxConstraints(minWidth: 120),
                            child: Text(
                              row.right,
                              textAlign: TextAlign.center,
                              style: const TextStyle(
                                fontSize: 14,
                                fontWeight: FontWeight.w700,
                                color: AppColors.titleText,
                              ),
                            ),
                          ),
                          const SizedBox(width: 8),
                          if (row.imageName != null)
                            Container(
                              width: 32,
                              height: 32,
                              decoration: BoxDecoration(
                                borderRadius: BorderRadius.circular(6),
                                image: DecorationImage(
                                  image: AssetImage(
                                    'assets/splash/${row.imageName}.jpeg',
                                  ),
                                  fit: BoxFit.cover,
                                ),
                              ),
                            )
                          else
                            const SizedBox(width: 32),
                        ],
                      ),
                    ],
                  ),
                )),
          ],
        ),
      ),
    );
  }

  Widget _buildPointsCard(
      {required String title,
      required String value,
      required String? levelKey,
      required String lang}) {
    final levelName =
        levelKey != null ? LocalizationService.translate(levelKey, lang) : '';
    return Card(
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
        side: const BorderSide(color: AppColors.cardBorder, width: 1),
      ),
      elevation: 0,
      color: AppColors.cardBackground,
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 20),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    title,
                    style: const TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.w700,
                      color: AppColors.titleText,
                    ),
                  ),
                  const SizedBox(height: 8),
                  Text(
                    value,
                    style: const TextStyle(
                      fontSize: 28,
                      fontWeight: FontWeight.w800,
                      color: AppColors.badgeBackground,
                    ),
                  ),
                ],
              ),
            ),
            if (levelName.isNotEmpty)
              Container(
                padding:
                    const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                decoration: BoxDecoration(
                  color: AppColors.badgeBackground.withOpacity(0.15),
                  borderRadius: BorderRadius.circular(10),
                ),
                child: Text(
                  levelName,
                  style: const TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.w800,
                    color: AppColors.badgeBackground,
                  ),
                ),
              ),
          ],
        ),
      ),
    );
  }
}

class _RowData {
  final String left;
  final String right;
  final String? imageName;
  _RowData({required this.left, required this.right, this.imageName});
}
