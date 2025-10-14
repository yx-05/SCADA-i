// components/CarbonChart.tsx
"use client";

import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';

const data = [
  { name: '0:00', level: 410 }, { name: '4:00', level: 420 },
  { name: '8:00', level: 450 }, { name: '12:00', level: 550 },
  { name: '16:00', level: 580 }, { name: '20:00', level: 500 },
];

const CarbonChart = () => (
    <div className="bg-white p-6 rounded-2xl shadow">
        <h3 className="font-semibold mb-4">Carbon Level Monitor</h3>
        <div style={{ width: '100%', height: 300 }}>
            <ResponsiveContainer>
                <LineChart data={data}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Line type="monotone" dataKey="level" stroke="#f59e0b" strokeWidth={2} dot={{ r: 4 }} activeDot={{ r: 8 }} />
                </LineChart>
            </ResponsiveContainer>
        </div>
    </div>
);

export default CarbonChart;