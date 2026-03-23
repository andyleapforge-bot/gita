import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import '../theme/colors.dart';
import '../routes.dart';
import '../services/language_service.dart';
import 'app_bar_title.dart';

class VitaAppBar extends StatelessWidget implements PreferredSizeWidget {
  final bool showBackButton;
  final bool showMenu;
  final bool showStreak;

  VitaAppBar(
      {this.showBackButton = false,
      this.showMenu = true,
      this.showStreak = false});

  @override
  Size get preferredSize => Size.fromHeight(kToolbarHeight);

  @override
  Widget build(BuildContext context) {
    return AppBar(
      backgroundColor: AppColors.navy,
      elevation: 0,
      title: AppBarTitle(),
      centerTitle: false,
      // Add extra left padding for pages without a back arrow
      titleSpacing: showBackButton ? 8.0 : 16.0,
      leading: showBackButton
          ? IconButton(
              icon: Icon(Icons.arrow_back, color: Colors.white),
              onPressed: () => Navigator.pop(context),
            )
          : null,
      leadingWidth: showBackButton ? 56 : 0,
      automaticallyImplyLeading: false,
      actions: [
        if (showStreak) _buildStreakWidget(),
        if (showMenu)
          PopupMenuButton<String>(
            color: AppColors.menuBackground,
            icon: Icon(Icons.more_vert, color: Colors.white),
            onSelected: (v) {
              if (v == 'bookmarks') {
                Navigator.pushNamed(context, Routes.bookmarks);
              }
              if (v == 'profile') {
                Navigator.pushNamed(context, Routes.profile);
              }
              if (v == 'gamification') {
                Navigator.pushNamed(context, Routes.gamification);
              }
            },
            itemBuilder: (_) {
              final langService = LanguageService();
              return [
                PopupMenuItem(
                  value: 'bookmarks',
                  child: Row(
                    children: [
                      Icon(Icons.bookmark,
                          color: AppColors.menuIconColor, size: 20),
                      SizedBox(width: 12),
                      Text(langService.translate('bookmarks'),
                          style: TextStyle(color: AppColors.menuIconColor)),
                    ],
                  ),
                ),
                PopupMenuItem(
                  value: 'profile',
                  child: Row(
                    children: [
                      Icon(Icons.person,
                          color: AppColors.menuIconColor, size: 20),
                      SizedBox(width: 12),
                      Text(langService.translate('profile'),
                          style: TextStyle(color: AppColors.menuIconColor)),
                    ],
                  ),
                ),
                PopupMenuItem(
                  value: 'gamification',
                  child: Row(
                    children: [
                      Icon(Icons.emoji_events,
                          color: AppColors.menuIconColor, size: 20),
                      SizedBox(width: 12),
                      Text(langService.translate('gamification'),
                          style: TextStyle(color: AppColors.menuIconColor)),
                    ],
                  ),
                ),
                PopupMenuDivider(),
                PopupMenuItem(
                  enabled: false,
                  child: Padding(
                    padding: EdgeInsets.symmetric(vertical: 4),
                    child: Text(langService.translate('language'),
                        style: TextStyle(
                            color: AppColors.menuIconColor,
                            fontWeight: FontWeight.w600,
                            fontSize: 12)),
                  ),
                ),
                PopupMenuItem(
                  child: Consumer<LanguageService>(
                    builder: (context, langService, _) {
                      return SizedBox(
                        width: 200,
                        child: Column(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            ListTile(
                              title: Text('English',
                                  style: TextStyle(
                                      color: AppColors.menuIconColor,
                                      fontSize: 14)),
                              trailing: langService.language == 'en'
                                  ? Icon(Icons.check,
                                      color: AppColors.gold, size: 20)
                                  : null,
                              onTap: () {
                                langService.setLanguage('en');
                                Navigator.pop(context);
                              },
                              contentPadding: EdgeInsets.zero,
                              dense: true,
                            ),
                            ListTile(
                              title: Text('हिंदी',
                                  style: TextStyle(
                                      color: AppColors.menuIconColor,
                                      fontSize: 14)),
                              trailing: langService.language == 'hi'
                                  ? Icon(Icons.check,
                                      color: AppColors.gold, size: 20)
                                  : null,
                              onTap: () {
                                langService.setLanguage('hi');
                                Navigator.pop(context);
                              },
                              contentPadding: EdgeInsets.zero,
                              dense: true,
                            ),
                          ],
                        ),
                      );
                    },
                  ),
                ),
              ];
            },
          ),
      ],
    );
  }

  Widget _buildStreakWidget() {
    final uid = FirebaseAuth.instance.currentUser?.uid;
    if (uid == null) return SizedBox.shrink();

    return StreamBuilder<DocumentSnapshot<Map<String, dynamic>>>(
      stream:
          FirebaseFirestore.instance.collection('users').doc(uid).snapshots(),
      builder: (context, snapshot) {
        if (!snapshot.hasData) return SizedBox.shrink();
        final data = snapshot.data?.data();
        final streak = (data?['streak'] as num?)?.toInt() ?? 0;

        return Padding(
          padding: const EdgeInsets.only(right: 8.0),
          child: Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(Icons.local_fire_department, color: Colors.orange, size: 24),
              SizedBox(width: 4),
              Text(
                streak.toString(),
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 16,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ],
          ),
        );
      },
    );
  }
}
