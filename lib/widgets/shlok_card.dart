import 'package:flutter/material.dart';
import '../theme/colors.dart';
import 'package:firebase_auth/firebase_auth.dart';
import '../services/user_service.dart';
import 'package:provider/provider.dart';
import '../services/language_service.dart';
import '../services/localization_service.dart';
import '../models/shlok.dart';

class ShlokCard extends StatelessWidget {
  final String shlokId;
  final int chapter;
  final double number;
  final String title;
  final String summary;
  final String poster;
  final bool isBookmarked;
  final VoidCallback? onBookmarkToggled;
  final Shlok? shlok;
  final String? searchQuery;

  ShlokCard(
      {required this.shlokId,
      required this.chapter,
      required this.number,
      required this.title,
      required this.summary,
      required this.poster,
      this.isBookmarked = false,
      this.onBookmarkToggled,
      this.shlok,
      this.searchQuery});

  @override
  Widget build(BuildContext context) {
    final langService = Provider.of<LanguageService>(context);

    // Use localized content if shlok object is available
    final displayTitle =
        shlok != null ? shlok!.getLocalizedTitle(langService.language) : title;
    final displaySummary = shlok != null
        ? shlok!.getLocalizedSummary(langService.language)
        : summary;

    String displayNumber = number.toString().replaceAll('.0', '');

    return Container(
      margin: EdgeInsets.only(bottom: 16),
      decoration: BoxDecoration(
        color: AppColors.cardBackground,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: AppColors.cardBorder, width: 2),
        boxShadow: [
          BoxShadow(
            color: AppColors.cardBorder.withOpacity(0.3),
            blurRadius: 4,
            offset: Offset(0, 2),
          ),
        ],
      ),
      child: InkWell(
        onTap: () => Navigator.pushNamed(context, '/shlok',
            arguments: {'id': shlokId, 'searchQuery': searchQuery}),
        borderRadius: BorderRadius.circular(16),
        child: Padding(
          padding: EdgeInsets.all(16),
          child: Row(
            children: [
              // Circular badge
              Container(
                width: 56,
                height: 56,
                decoration: BoxDecoration(
                  color: AppColors.badgeBackground,
                  shape: BoxShape.circle,
                ),
                child: Center(
                  child: Text(
                    '$chapter.$displayNumber',
                    style: TextStyle(
                      color: AppColors.badgeText,
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
              ),
              SizedBox(width: 16),
              // Title and summary
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      displayTitle,
                      style: TextStyle(
                        color: AppColors.titleText,
                        fontSize: 16,
                        fontWeight: FontWeight.bold,
                      ),
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                    ),
                    SizedBox(height: 6),
                    Text(
                      displaySummary,
                      style: TextStyle(
                        color: AppColors.summaryText,
                        fontSize: 14,
                        height: 1.3,
                      ),
                      maxLines: 2,
                      overflow: TextOverflow.ellipsis,
                    ),
                  ],
                ),
              ),
              SizedBox(width: 8),
              // Icons
              Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  IconButton(
                    onPressed: () {
                      Navigator.pushNamed(context, '/shlok', arguments: {
                        'id': shlokId,
                        'searchQuery': searchQuery
                      });
                    },
                    icon: Icon(Icons.play_arrow,
                        color: AppColors.iconColor, size: 28),
                    padding: EdgeInsets.zero,
                    constraints: BoxConstraints(),
                  ),
                  SizedBox(width: 12),
                  IconButton(
                    onPressed: () async {
                      final user = FirebaseAuth.instance.currentUser;
                      if (user == null) {
                        final langService = Provider.of<LanguageService>(
                            context,
                            listen: false);
                        ScaffoldMessenger.of(context).showSnackBar(
                          SnackBar(
                              content: Text(langService.language == 'hi'
                                  ? 'बुकमार्क करने के लिए कृपया लॉगिन करें'
                                  : 'Please login to bookmark')),
                        );
                        return;
                      }
                      try {
                        final langService = Provider.of<LanguageService>(
                            context,
                            listen: false);
                        if (isBookmarked) {
                          await UserService().removeBookmark(user.uid, shlokId);
                          ScaffoldMessenger.of(context).showSnackBar(
                            SnackBar(
                                content: Text(langService.language == 'hi'
                                    ? 'बुकमार्क से हटाया गया'
                                    : 'Removed from bookmarks')),
                          );
                        } else {
                          await UserService().addBookmark(user.uid, shlokId);
                          ScaffoldMessenger.of(context).showSnackBar(
                            SnackBar(
                                content: Text(langService.language == 'hi'
                                    ? 'बुकमार्क में जोड़ा गया'
                                    : 'Added to bookmarks')),
                          );
                        }
                      } catch (_) {
                        // keep UI responsive even if backend fails
                      }
                      if (onBookmarkToggled != null) onBookmarkToggled!();
                    },
                    icon: Icon(
                      isBookmarked ? Icons.bookmark : Icons.bookmark_border,
                      color: isBookmarked
                          ? AppColors.badgeBackground
                          : AppColors.iconColor,
                      size: 26,
                    ),
                    padding: EdgeInsets.zero,
                    constraints: BoxConstraints(),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}
