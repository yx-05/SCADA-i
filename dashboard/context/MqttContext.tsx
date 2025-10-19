'use client';

import React, { createContext, useContext, useEffect, useState } from 'react';
import { SensorMessage } from '../types/sensors';
import { getMqttClient } from '../lib/mqttClient';

interface MqttContextType {
  sensorData: SensorMessage | null;
  totalOccupancy: number;
}

const MqttContext = createContext<MqttContextType>({ sensorData: null, totalOccupancy: 0});

// Map to store each device data
const sensorDataMap = new Map<string, SensorMessage>();

export const MqttProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [sensorData, setSensorData] = useState<SensorMessage | null>(null);
  const [totalOccupancy, setTotalOccupancy] = useState(0);

  useEffect(() => {


    const client = getMqttClient();

    // 1. Create a named function for the message handler
    const messageHandler = (topic: string, payload: Buffer) => {
      const message = payload.toString();
      console.log('Received message inside MqttProvider:', message, topic);
      try {
        const parsedData = JSON.parse(message.toString());
        const [_, roomId, __, deviceId] = topic.split('/');

        const sensorMessage: SensorMessage = {
          ...parsedData,
          topic,
          roomId,
          deviceId,
        };

        const key = `${roomId}-${deviceId}`;
        sensorDataMap.set(key, sensorMessage);

        // Compute totals
        let occ = 0;
        for (const [, data] of sensorDataMap) {
          occ += data.occupancy;
        }

        setSensorData(sensorMessage)
        setTotalOccupancy(occ);
      } catch (error) {
        console.error("Failed to parse incoming JSON message:", error)
      }
    };

    // 2. Add the specific handler as a listener
    client.on('message', messageHandler);

    // 3. The cleanup function now removes only that specific handler
    return () => {
      client.off('message', messageHandler);
    };
  }, []); // Empty dependency array is correct

  return (
    <MqttContext.Provider value={{ sensorData, totalOccupancy }}>
      {children}
    </MqttContext.Provider>
  );
};

// No changes to the hook
export function useMqtt() {
  return useContext(MqttContext);
}