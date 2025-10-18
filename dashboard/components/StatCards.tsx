// components/StatCards.tsx
"use client"
import React from 'react';
import { useMqtt } from '@/context/MqttContext';

const statData = [
  { title: 'Carbon Level', value: '420', unit: 'ppm', color: 'bg-green-100', textColor: 'text-green-800' },
  { title: 'Power Consumption', value: '6430', unit: 'W', color: 'bg-yellow-100', textColor: 'text-yellow-800' },
  { title: 'Occupancy', value: '10/18', unit: '', color: 'bg-blue-100', textColor: 'text-blue-800' },
  { title: 'Energy Saved Today', value: '2200', unit: 'W', color: 'bg-teal-100', textColor: 'text-teal-800' },
];

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
  const { sensorData } = useMqtt();
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
      {statData.map((stat, index) => (
        <StatCard key={index} {...stat} />
      ))}
    </div>
  );
};

export default StatCards;