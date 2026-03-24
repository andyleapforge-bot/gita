import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:firebase_auth/firebase_auth.dart';
import '../theme/colors.dart';
import '../widgets/vita_app_bar.dart';
import '../services/shlok_service.dart';
import '../services/video_link_service.dart';
import '../services/user_service.dart';
import '../services/language_service.dart';
import '../services/localization_service.dart';
import '../widgets/shlok_video_player.dart';
import '../models/shlok.dart';
import 'package:flutter/rendering.dart';
import 'package:share_plus/share_plus.dart';
import 'package:screenshot/screenshot.dart';
import 'dart:io';
import 'package:path_provider/path_provider.dart';
import '../routes.dart';

class ShlokDetailPage extends StatefulWidget {
  @override
  _ShlokDetailPageState createState() => _ShlokDetailPageState();
}

class _ShlokDetailPageState extends State<ShlokDetailPage> {
  // expects arguments via Navigator: {'id': 'shlokId'}
  final GlobalKey _screenshotKey = GlobalKey();
  final _videoLinkService = VideoLinkService();
  final _userService = UserService();
  final ScreenshotController _screenshotController = ScreenshotController();

  Future<void> _shareScreenshot(
      BuildContext sourceContext, Shlok shlok, String? videoUrl) async {
    try {
      // Build full content offscreen and capture as image
      final bytes = await _screenshotController.captureFromWidget(
        Material(
          color: AppColors.cream,
          child: Padding(
            padding: const EdgeInsets.all(16.0),
            child: _buildShareableContent(shlok, videoUrl),
          ),
        ),
        pixelRatio: 2.0,
      );

      // Write to temp file
      final dir = await getTemporaryDirectory();
      final file = File('${dir.path}/shlok_share.png');
      await file.writeAsBytes(bytes);

      // Award share points (once per day)
      await _awardSharePoints();

      // Share image (WhatsApp will appear if installed)
      Rect? shareOrigin;
      try {
        final renderObject = sourceContext.findRenderObject();
        if (renderObject is RenderBox) {
          final size = MediaQuery.of(sourceContext).size;
          final isIpad = Platform.isIOS && size.shortestSide >= 600;
          if (isIpad) {
            shareOrigin = renderObject.localToGlobal(Offset.zero) &
                renderObject.size;
          }
        }
      } catch (_) {}

      await Share.shareXFiles(
        [XFile(file.path)],
        text: 'VitaGita',
        sharePositionOrigin: shareOrigin,
      );
    } catch (e) {
      debugPrint('[share] failed: ');
      if (context.mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Share failed. Please try again.')),
        );
      }
    }
  }

  /// Award share points (50 points, once per day).
  Future<void> _awardSharePoints() async {
    final uid = FirebaseAuth.instance.currentUser?.uid;
    if (uid == null) return;

    try {
      final isEligible =
          await _userService.isActivityEligibleToday(uid, 'share');
      if (isEligible) {
        await _userService.logActivityAndAwardPoints(uid, 'share', 50);
        debugPrint('[points] awarded +50 for sharing to $uid');
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(
              content: Text('+50 Points! Share Reward'),
              duration: Duration(seconds: 3),
              backgroundColor: Color(0xFF6A5AAE),
            ),
          );
        }
      } else {
        debugPrint('[points] share already awarded today for $uid');
      }
    } catch (e) {
      debugPrint('[points] failed to award share points: $e');
    }
  }

  Widget _buildShareableContent(Shlok shlok, String? videoUrl) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      mainAxisSize: MainAxisSize.min,
      children: [
        // Title only (omit the share button in the capture)
        Text(
          shlok.title,
          style: const TextStyle(
            fontSize: 20,
            fontWeight: FontWeight.bold,
          ),
        ),
        const SizedBox(height: 12),
        // Meta row
        Row(
          children: [
            const Icon(Icons.person, size: 16),
            const SizedBox(width: 6),
            Text(shlok.speaker),
            const SizedBox(width: 12),
            const Icon(Icons.category, size: 16),
            const SizedBox(width: 6),
            Text(shlok.theme),
            const SizedBox(width: 12),
            const Icon(Icons.star, size: 16, color: Color(0xFFD4A843)),
            const SizedBox(width: 6),
            Text('${shlok.star}'),
          ],
        ),
        const SizedBox(height: 8),
        if (shlok.summary.isNotEmpty) ...[
          Text(shlok.summary),
          const SizedBox(height: 8),
        ],
        if (shlok.keywords.isNotEmpty) ...[
          Wrap(
            spacing: 8,
            runSpacing: 6,
            children: shlok.keywords
                .map((k) => Container(
                      padding: const EdgeInsets.symmetric(
                          horizontal: 10, vertical: 6),
                      decoration: BoxDecoration(
                        color: AppColors.chipBackground,
                        borderRadius: BorderRadius.circular(16),
                        border: Border.all(color: AppColors.searchBorder),
                      ),
                      child: Text(k, style: const TextStyle(fontSize: 12)),
                    ))
                .toList(),
          ),
          const SizedBox(height: 12),
        ],
        if (videoUrl != null && videoUrl.isNotEmpty)
          // For share image, prefer poster preview if available instead of video
          if (shlok.posterImageUrl.isNotEmpty)
            ClipRRect(
              borderRadius: BorderRadius.circular(8),
              child: Image.network(
                shlok.posterImageUrl,
                height: 200,
                width: double.infinity,
                fit: BoxFit.cover,
              ),
            )
          else
            const SizedBox.shrink()
        else if (shlok.posterImageUrl.isNotEmpty)
          ClipRRect(
            borderRadius: BorderRadius.circular(8),
            child: Image.network(
              shlok.posterImageUrl,
              height: 200,
              width: double.infinity,
              fit: BoxFit.cover,
            ),
          )
        else
          Container(
            height: 200,
            decoration: BoxDecoration(
              color: Colors.black12,
              borderRadius: BorderRadius.circular(8),
            ),
            alignment: Alignment.center,
            child: const Text('No media available'),
          ),
      ],
    );
  }

  /// Award search points (10 points, once per day) when user views a shlok from search results
  /// Only awards points if searchQuery is provided (user came from search)
  Future<void> _awardSearchPoints(String? searchQuery) async {
    // Only award search points if user came from search results
    if (searchQuery == null || searchQuery.isEmpty) return;

    final uid = FirebaseAuth.instance.currentUser?.uid;
    if (uid == null) return;

    try {
      final isEligible =
          await _userService.isActivityEligibleToday(uid, 'search');
      if (isEligible) {
        await _userService.logActivityAndAwardPoints(uid, 'search', 10);
        debugPrint('[points] awarded +10 for search/click to $uid');
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(
              content: Text('+10 Points! Shlok Search Reward'),
              duration: Duration(seconds: 3),
              backgroundColor: Color(0xFF6A5AAE),
            ),
          );
        }
      } else {
        debugPrint('[points] search already awarded today for $uid');
      }
    } catch (e) {
      debugPrint('[points] failed to award search points: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    final args =
        ModalRoute.of(context)?.settings.arguments as Map<String, dynamic>?;
    final id = args?['id'] as String? ?? '';
    final searchQuery = args?['searchQuery'] as String?;
    final langService = Provider.of<LanguageService>(context);

    return WillPopScope(
      onWillPop: () async {
        // From Detail, back should go to Home
        Navigator.pushReplacementNamed(context, Routes.home);
        return false;
      },
      child: Scaffold(
        backgroundColor: AppColors.cream,
        // Match the Sign Up navbar style, with only a back arrow
        appBar: VitaAppBar(showBackButton: true, showMenu: false),
        body: FutureBuilder<Shlok?>(
          future:
              ShlokService().getShlokById(id, language: langService.language),
          builder: (context, snapshot) {
            if (snapshot.connectionState != ConnectionState.done)
              return Center(child: CircularProgressIndicator());
            final shlok = snapshot.data;
            if (shlok == null)
              return Center(
                  child: Text(LocalizationService.translate(
                      'not_found', langService.language)));
            // Award search points only when user views a shlok from search results
            WidgetsBinding.instance.addPostFrameCallback((_) {
              _awardSearchPoints(searchQuery);
            });
            return FutureBuilder<String?>(
              future: _videoLinkService.getVideoUrlForShlok(shlok),
              builder: (context, videoSnap) {
                final videoUrl = videoSnap.data;
                return SingleChildScrollView(
                  padding: EdgeInsets.all(16),
                  child: RepaintBoundary(
                    key: _screenshotKey,
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        // Title + Bookmark
                        Row(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Expanded(
                              child: Text(
                                shlok.getLocalizedTitle(langService.language),
                                style: TextStyle(
                                  fontSize: 20,
                                  fontWeight: FontWeight.bold,
                                  color: AppColors.navy,
                                ),
                              ),
                            ),
                            Builder(
                              builder: (buttonContext) => IconButton(
                                onPressed: () => _shareScreenshot(
                                    buttonContext, shlok, videoUrl),
                                icon: Icon(Icons.share,
                                    color: AppColors.iconColor),
                              ),
                            ),
                          ],
                        ),
                        SizedBox(height: 12),
                        // Meta row
                        Row(
                          children: [
                            Icon(Icons.person,
                                size: 16, color: AppColors.iconColor),
                            SizedBox(width: 6),
                            Text(
                                shlok.getLocalizedSpeaker(langService.language),
                                style: TextStyle(color: AppColors.navy)),
                            SizedBox(width: 12),
                            Icon(Icons.category,
                                size: 16, color: AppColors.iconColor),
                            SizedBox(width: 6),
                            Text(shlok.getLocalizedTheme(langService.language),
                                style: TextStyle(color: AppColors.navy)),
                            SizedBox(width: 12),
                            Icon(Icons.star,
                                size: 16, color: AppColors.badgeBackground),
                            SizedBox(width: 6),
                            Text('${shlok.star}',
                                style: TextStyle(color: AppColors.navy)),
                          ],
                        ),
                        SizedBox(height: 8),

                        // Summary line under meta
                        if (shlok.summary.isNotEmpty) ...[
                          Text(
                            shlok.getLocalizedSummary(langService.language),
                            style: TextStyle(color: AppColors.navy),
                          ),
                          SizedBox(height: 8),
                        ],

                        // Keywords placed directly under the summary, before media
                        if (shlok.keywords.isNotEmpty) ...[
                          Wrap(
                            spacing: 8,
                            runSpacing: 6,
                            children: shlok
                                .getLocalizedKeywords(langService.language)
                                .map((k) => Container(
                                      padding: EdgeInsets.symmetric(
                                          horizontal: 10, vertical: 6),
                                      decoration: BoxDecoration(
                                        color: AppColors.chipBackground,
                                        borderRadius: BorderRadius.circular(16),
                                        border: Border.all(
                                            color: AppColors.searchBorder),
                                      ),
                                      child: Text(
                                        k,
                                        style: TextStyle(
                                            color: AppColors.chipText,
                                            fontSize: 12),
                                      ),
                                    ))
                                .toList(),
                          ),
                          SizedBox(height: 12),
                        ],
                        // Media section after keywords
                        if (videoSnap.connectionState != ConnectionState.done)
                          Container(
                            height: 200,
                            color: Colors.black12,
                            alignment: Alignment.center,
                            child: CircularProgressIndicator(),
                          )
                        else if (videoUrl != null && videoUrl.isNotEmpty)
                          ShlokVideoPlayer(url: videoUrl, shlokId: shlok.id)
                        else if (shlok.posterImageUrl.isNotEmpty)
                          ClipRRect(
                            borderRadius: BorderRadius.circular(8),
                            child: Image.network(
                              shlok.posterImageUrl,
                              height: 200,
                              width: double.infinity,
                              fit: BoxFit.cover,
                            ),
                          )
                        else
                          Container(
                            height: 200,
                            decoration: BoxDecoration(
                              color: Colors.black12,
                              borderRadius: BorderRadius.circular(8),
                            ),
                            alignment: Alignment.center,
                            child: Text('No media available'),
                          ),
                        // Removed Sanskrit & Translation sections per request
                      ],
                    ),
                  ),
                );
              },
            );
          },
        ),
      ),
    );
  }
}
