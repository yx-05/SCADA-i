// components/AiActions.tsx
"use client";

import React, { useState } from 'react';
import ToggleSwitch from './ToggleSwitch';

const actionsData = [
  { text: 'Reduce AC by 15% at 9 p.m.', tag: 'scheduled', tagColor: 'bg-orange-100 text-orange-800', savings: '' },
  { text: 'Auto-dim lights in Row A', tag: 'recommended', tagColor: 'bg-blue-100 text-blue-800', savings: 'Saves 40W' },
  { text: 'Auto-close non-active microwave', tag: 'active', tagColor: 'bg-green-100 text-green-800', savings: 'Saves 120W' },
];

const AiActions = () => {
  const [isAiActive, setIsAiActive] = useState(true);

  return (
    <div className="bg-white p-6 rounded-2xl shadow">
      <h3 className="font-semibold mb-4">AI Actions & Predictions</h3>
      <div className="space-y-3 mb-6">
        {actionsData.map((action, index) => (
          <div key={index} className="bg-gray-50 p-3 rounded-lg flex justify-between items-center">
            <div>
              <p className="font-medium text-sm">{action.text}</p>
              {action.savings && <p className="text-xs text-gray-500">{action.savings}</p>}
            </div>
            <span className={`text-xs font-semibold px-2 py-1 rounded-full ${action.tagColor}`}>
              {action.tag}
            </span>
          </div>
        ))}
      </div>
      <div className="border-t pt-4 flex justify-between items-center">
        <p className="font-semibold">AI Optimize Active</p>
        <ToggleSwitch 
          toggled={isAiActive} 
          onClick={() => setIsAiActive(!isAiActive)} // Directly update the state on click
          bgColor="bg-blue-600"
        />
      </div>
    </div>
  );
};

export default AiActions;