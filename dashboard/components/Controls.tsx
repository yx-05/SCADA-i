// components/Controls.tsx
"use client";

import { AirVent, Laptop, Lightbulb, Microwave } from "lucide-react";
import React, { useState } from "react";
import ToggleSwitch from "./ToggleSwitch";
import { useMqtt } from "@/context/MqttContext";

const initialControlData = [
  {
    id: 1,
    icon: AirVent,
    name: "AC Units",
    status: "24/32 active • 3200W",
    toggled: true,
  },
  {
    id: 2,
    icon: Laptop,
    name: "Computers",
    status: "23/60 active • 2350W",
    toggled: true,
  },
  {
    id: 3,
    icon: Lightbulb,
    name: "Lights",
    status: "8/12 active • 220W",
    toggled: true,
  },
  {
    id: 4,
    icon: Microwave,
    name: "Microwave",
    status: "0/1 active • 0W",
    toggled: false,
  },
];

const Controls = () => {
  const [controls, setControls] = useState(initialControlData);
  const { publish } = useMqtt();

const handleToggle = (id: number) => {
    setControls(currentControls =>
      currentControls.map(control => {
        if (control.id === id) {
          const newToggled = !control.toggled;

          // 🟢 Publish MQTT command here
          const topic = `room/1/manual_override/response`;
          const payload = {
            deviceId: id,
            name: control.name,
            toggled: newToggled,
            timestamp: new Date().toISOString(),
          };

          publish(topic, payload);
          console.log(`Published to ${topic}:`, payload);

          return { ...control, toggled: newToggled };
        }
        return control;
      })
    );
  };

  return (
    <div className="bg-white p-6 rounded-2xl shadow">
      <h3 className="font-semibold mb-4">Manual Controller</h3>
      <div className="space-y-4">
        {controls.map((item) => (
          <div key={item.id} className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <item.icon className="text-gray-600" size={24} />
              <div>
                <p className="font-medium">{item.name}</p>
                <p className="text-xs text-gray-500">{item.status}</p>
              </div>
            </div>
            {/* Pass the current state and the handler to the ToggleSwitch */}
            <ToggleSwitch
              toggled={item.toggled}
              onClick={() => handleToggle(item.id)}
            />
          </div>
        ))}
      </div>
    </div>
  );
};

export default Controls;
