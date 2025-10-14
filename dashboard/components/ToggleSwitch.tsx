// components/ToggleSwitch.tsx
"use client";

import React from 'react';

// Define the props: its current state and what to do when clicked
interface ToggleSwitchProps {
  toggled: boolean;
  onClick: () => void;
  bgColor?: string; 
}

const ToggleSwitch = ({ toggled, onClick, bgColor = 'bg-green-500' }: ToggleSwitchProps) => (
  <button 
    onClick={onClick}
    className={`w-12 h-6 flex items-center rounded-full p-1 cursor-pointer transition-colors duration-300 ease-in-out ${toggled ? bgColor : 'bg-gray-300'}`}
    aria-pressed={toggled}
  >
    <div 
      className={`bg-white w-5 h-5 rounded-full shadow-md transform transition-transform duration-300 ease-in-out ${toggled ? 'translate-x-5' : ''}`}
    />
  </button>
);

export default ToggleSwitch;