// components/DeviceOverview.tsx
"use client";

import React from 'react';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts';

const data = [
  { name: 'AC Units', value: 3200 },
  { name: 'Computers', value: 2350 },
  { name: 'Lights', value: 220 },
  { name: 'Microwaves', value: 400 },
];

const DeviceOverview = () => {
  return (
    <div className="bg-white p-6 rounded-2xl shadow">
      <h3 className="font-semibold mb-4">Device Status Overview</h3>
      <div style={{ width: '100%', height: 300 }}>
        <ResponsiveContainer>
          <BarChart data={data} margin={{ top: 5, right: 20, left: -10, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip cursor={{fill: 'rgba(243, 244, 246, 0.5)'}} />
            <Bar dataKey="value" fill="#60a5fa" barSize={60} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default DeviceOverview;