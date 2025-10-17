'use client';

import React, { createContext, useContext, useEffect, useState } from 'react';
import { SensorData } from '../types/sensors';
import { getMqttClient } from '../lib/mqttClient';

// No changes to the context creation
const MqttContext = createContext<{ sensorData: SensorData | null }>({ sensorData: null });

export const MqttProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [sensorData, setSensorData] = useState<SensorData | null>(null);

  useEffect(() => {
    const client = getMqttClient();

    // 1. Create a named function for the message handler
    const messageHandler = (topic: string, payload: Buffer) => {
      const message = payload.toString();
      console.log('Received message inside MqttProvider:', message);
      try {
        const parsedData: SensorData = JSON.parse(message)
        
        setSensorData(parsedData)
      } catch (error){
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
    <MqttContext.Provider value={{ sensorData }}>
      {children}
    </MqttContext.Provider>
  );
};

// No changes to the hook
export function useMqtt() {
  return useContext(MqttContext);
}