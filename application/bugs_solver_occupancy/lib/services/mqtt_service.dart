import 'dart:convert';
import 'dart:async';
import 'package:mqtt_client/mqtt_client.dart';
import 'package:mqtt_client/mqtt_server_client.dart';

class MQTTService {
  // Singleton instance
  static final MQTTService _instance = MQTTService._internal();
  factory MQTTService() => _instance;

  late MqttServerClient client;

  // 🔹 Flutter listens to this stream
  final _controller = StreamController<Map<String, dynamic>>.broadcast();
  Stream<Map<String, dynamic>> get dataStream => _controller.stream;

  MQTTService._internal();

  Future<void> connect() async {
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

    // ✅ Subscribe to both sensor and override response topics
    client.subscribe('room/+/device/+/sensor', MqttQos.atLeastOnce);
    client.subscribe('room/+/manual_override/response', MqttQos.atLeastOnce);

    // ✅ Listen for incoming messages
    client.updates!.listen((List<MqttReceivedMessage<MqttMessage?>>? messages) {
      final recMess = messages![0].payload as MqttPublishMessage;
      final topic = messages[0].topic;
      final payload =
      MqttPublishPayload.bytesToStringAsString(recMess.payload.message);

      try {
        final Map<String, dynamic> data = jsonDecode(payload);
        data['topic'] = topic; // attach topic info for filtering if needed
        print('📡 [MQTT] Received: $data');
        _controller.add(data);
      } catch (e) {
        print('⚠️ Error decoding JSON: $e');
      }
    });
  }

  // 🔹 Publish messages to IoT
  void publish(String topic, Map<String, dynamic> payload) {
    if (client.connectionStatus?.state != MqttConnectionState.connected) {
      print("⚠️ MQTT not connected — cannot publish");
      return;
    }
    final builder = MqttClientPayloadBuilder();
    builder.addUTF8String(jsonEncode(payload));
    client.publishMessage(topic, MqttQos.atLeastOnce, builder.payload!);
    print("📤 Published to $topic: $payload");
  }

  void onConnected() {
    print('✅ Connected to MQTT Broker');
  }

  void onDisconnected() {
    print('⚠️ Disconnected from MQTT Broker');
  }

  void disconnect() {
    client.disconnect();
  }
}
