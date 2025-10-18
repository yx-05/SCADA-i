import mqtt, { MqttClient } from 'mqtt';

let client: MqttClient | null = null;

export function getMqttClient(): MqttClient {
    if (!client) {
        // Connect only once
        client = mqtt.connect('ws://192.168.0.105:8083/mqtt'); //change this

        client.on('connect', () => {
            console.log('MQTT Connected');
            client?.subscribe('room/+/device/+/sensor', (err) => {
                if (err) console.error('Subscription error:', err);
                else console.log('Subscribed successfully');
            });

            // client?.subscribe('room/room1/device/1/sensor'); // change this
        });

        client.on('error', (err) => {
            console.error('MQTT Error:', err);
        });
    }
    return client;
}
