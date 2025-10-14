import 'dart:convert';
import 'dart:async';
import 'package:mqtt_client/mqtt_client.dart';
import 'package:mqtt_client/mqtt_server_client.dart';

class MQTTService {
  // singleton pattern
  static final MQTTService _instance = MQTTService._internal();
  factory MQTTService() => _instance;

  late MqttServerClient client;

  // ✅ this is the stream Flutter listens to
  final _controller = StreamController<Map<String, dynamic>>.broadcast();
  Stream<Map<String, dynamic>> get dataStream => _controller.stream;

  MQTTService._internal();

  Future<void> connect() async {
    // ⚙️ change this to your broker’s IP or hostname
    client = MqttServerClient('192.168.1.123', 'flutter_client');
    client.port = 1883;
    client.keepAlivePeriod = 20;
    client.logging(on: false);
    client.onConnected = onConnected;
    client.onDisconnected = onDisconnected;

    try {
      print('🔌 Connecting to MQTT broker...');
      await client.connect();
    } catch (e) {
      print('❌ MQTT connection failed: $e');
      client.disconnect();
      return;
    }

    // ✅ subscribe to your topic pattern
    client.subscribe('room/+/device/+/sensor', MqttQos.atLeastOnce);

    // ✅ listen for new messages
    client.updates!.listen((List<MqttReceivedMessage<MqttMessage?>>? messages) {
      final recMess = messages![0].payload as MqttPublishMessage;
      final payload =
      MqttPublishPayload.bytesToStringAsString(recMess.payload.message);

      try {
        final Map<String, dynamic> data = jsonDecode(payload);
        print('📡 [MQTT] Received: $data');
        _controller.add(data); // push data to Flutter UI
      } catch (e) {
        print('⚠️ Error decoding JSON: $e');
      }
    });
  }

  void onConnected() {
    print('✅ Connected to MQTT Broker');
  }

  void onDisconnected() {
    print('⚠️ Disconnected from MQTT Broker');
  }
}
