import 'package:flutter/material.dart';
import 'package:video_player/video_player.dart';
import 'package:firebase_auth/firebase_auth.dart';
import '../services/user_service.dart';

class ShlokVideoPlayer extends StatefulWidget {
  final String url;
  final String? shlokId; // ID of shlok for activity tracking
  final double? aspectRatio;

  const ShlokVideoPlayer({
    super.key,
    required this.url,
    this.shlokId,
    this.aspectRatio,
  });

  @override
  State<ShlokVideoPlayer> createState() => _ShlokVideoPlayerState();
}

class _ShlokVideoPlayerState extends State<ShlokVideoPlayer> {
  late VideoPlayerController _controller;
  bool _initialized = false;
  bool _error = false;
  bool _listenPointsAwarded =
      false; // Track if points already awarded for this shlok
  bool _watchedEnough = false; // Track if user watched for 5+ seconds
  final UserService _userService = UserService();

  @override
  void initState() {
    super.initState();
    _controller = VideoPlayerController.networkUrl(Uri.parse(widget.url))
      ..initialize().then((_) {
        setState(() {
          _initialized = true;
        });
        // Listen for video playback to check if 5 seconds watched
        _controller.addListener(_checkVideoProgress);
      }).catchError((_) {
        setState(() {
          _error = true;
        });
      });
  }

  /// Check if user has watched for 5+ seconds and award points
  void _checkVideoProgress() {
    if (!_listenPointsAwarded &&
        _controller.value.isInitialized &&
        _controller.value.isPlaying &&
        _controller.value.position >= const Duration(seconds: 5)) {
      _awardListenPoints();
    }
  }

  /// Award points for watching 5+ seconds of shlok
  Future<void> _awardListenPoints() async {
    _listenPointsAwarded = true;
    final uid = FirebaseAuth.instance.currentUser?.uid;
    final shlokId = widget.shlokId;

    if (uid == null || shlokId == null || shlokId.isEmpty) return;

    try {
      // Check if this shlok was already listened to
      final isEligible =
          await _userService.isActivityEligibleToday(uid, 'listen_$shlokId');
      // Note: reuse the per-day eligibility check keyed by shlokId
      final doc = await _userService.getDoc(uid);
      final activities = (doc?['activities'] as Map<String, dynamic>?) ?? {};
      final listenKey = 'listen:$shlokId';

      if (!activities.containsKey(listenKey)) {
        debugPrint('[points] awarding +20 for listening to shlok $shlokId');
        await _userService.logListenActivityAndAwardPoints(uid, shlokId, 20);
        debugPrint('[points] awarded +20 for listening to shlok $shlokId');
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(
              content: Text('+20 Points! Shlok Listen Reward'),
              duration: Duration(seconds: 3),
              backgroundColor: Color(0xFF6A5AAE),
            ),
          );
        }
      } else {
        debugPrint('[points] shlok $shlokId already listened, no points');
      }
    } catch (e) {
      debugPrint('[points] error awarding listen points: $e');
    }
  }

  @override
  void dispose() {
    _controller.removeListener(_checkVideoProgress);
    _controller.dispose();
    super.dispose();
  }

  void _togglePlay() {
    if (!_initialized) return;
    setState(() {
      if (_controller.value.isPlaying) {
        _controller.pause();
      } else {
        _controller.play();
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    if (_error) {
      return Container(
        height: 200,
        color: Colors.black12,
        alignment: Alignment.center,
        child: const Text('Video unavailable'),
      );
    }

    if (!_initialized) {
      return Container(
        height: 200,
        color: Colors.black12,
        alignment: Alignment.center,
        child: const CircularProgressIndicator(),
      );
    }

    // Default to 16:9 if aspectRatio is unavailable or odd
    final ar = widget.aspectRatio ??
        (_controller.value.isInitialized && _controller.value.aspectRatio > 0
            ? _controller.value.aspectRatio
            : 16 / 9);

    return Column(
      children: [
        AspectRatio(
          aspectRatio: ar,
          child: Stack(
            alignment: Alignment.center,
            children: [
              VideoPlayer(_controller),
              Positioned(
                bottom: 8,
                left: 8,
                right: 8,
                child: VideoProgressIndicator(
                  _controller,
                  allowScrubbing: true,
                  padding: const EdgeInsets.symmetric(vertical: 4),
                ),
              ),
              GestureDetector(
                onTap: _togglePlay,
                child: AnimatedOpacity(
                  opacity: _controller.value.isPlaying ? 0.0 : 1.0,
                  duration: const Duration(milliseconds: 200),
                  child: Container(
                    decoration: BoxDecoration(
                      color: Colors.black45,
                      shape: BoxShape.circle,
                    ),
                    padding: const EdgeInsets.all(12),
                    child: Icon(
                      _controller.value.isPlaying
                          ? Icons.pause
                          : Icons.play_arrow,
                      color: Colors.white,
                      size: 36,
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
      ],
    );
  }
}
