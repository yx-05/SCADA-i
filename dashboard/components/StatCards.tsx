// components/StatCards.tsx
"use client"
import React from 'react';
import { useMqtt } from '@/context/MqttContext';

// 1. Define the "contract" for the props using an interface
interface StatCardProps {
  title: string;
  value: string;
  unit: string;
  color: string;
  textColor: string;
}

// 2. Apply the interface to your component's props
const StatCard = ({ title, value, unit, color, textColor }: StatCardProps) => (
  <div className={`${color} p-6 rounded-2xl`}>
    <p className={`text-sm font-medium ${textColor}`}>{title}</p>
    <div className="flex items-baseline space-x-2 mt-2">
      <h2 className={`text-4xl font-bold ${textColor}`}>{value}</h2>
      {unit && <span className={`text-lg font-medium ${textColor}`}>{unit}</span>}
    </div>
  </div>
);

const StatCards = () => {
  const { sensorData, totalOccupancy } = useMqtt();

  // --- Safely extract values from sensorData ---
  const carbonLevel = 420;      // e.g., CO2
  const powerUsage = sensorData?.power_usage ?? 0;        // watts
  const occupancy = totalOccupancy?? 0;          // number of people
  const totalSeats = 18;                                 // Example static value
  const energySaved = 2200;      // Example if included

  const statData: StatCardProps[] = [
    {
      title: "Carbon Level",
      value: carbonLevel.toString(),
      unit: "ppm",
      color: "bg-green-100",
      textColor: "text-green-800",
    },
    {
      title: "Power Consumption",
      value: powerUsage.toString(),
      unit: "W",
      color: "bg-yellow-100",
      textColor: "text-yellow-800",
    },
    {
      title: "Occupancy",
      value: `${occupancy}/${totalSeats}`,
      unit: "",
      color: "bg-blue-100",
      textColor: "text-blue-800",
    },
    {
      title: "Energy Saved Today",
      value: energySaved.toString(),
      unit: "W",
      color: "bg-teal-100",
      textColor: "text-teal-800",
    },
  ];

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
      {statData.map((stat, index) => (
        <StatCard key={index} {...stat} />
      ))}
    </div>
  );
};

export default StatCards;