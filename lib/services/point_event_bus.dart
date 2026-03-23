import 'dart:async';

/// Simple EventBus to notify about point changes across the app
class PointEventBus {
  static final PointEventBus _instance = PointEventBus._internal();

  factory PointEventBus() {
    return _instance;
  }

  PointEventBus._internal();

  final _pointsController = StreamController<int>.broadcast();

  /// Stream of point changes
  Stream<int> get pointsStream => _pointsController.stream;

  /// Notify that points have changed (with new total)
  void notifyPointsChanged(int newPoints) {
    _pointsController.add(newPoints);
  }

  void dispose() {
    _pointsController.close();
  }
}
