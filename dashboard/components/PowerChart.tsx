// components/PowerChart.tsx
"use client";

import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';

const data = [
  { name: '0:00', consumption: 400, savings: 240 },
  { name: '4:00', consumption: 300, savings: 139 },
  { name: '8:00', consumption: 450, savings: 580 },
  { name: '12:00', consumption: 680, savings: 390 },
  { name: '16:00', consumption: 720, savings: 480 },
  { name: '20:00', consumption: 500, savings: 380 },
];

const PowerChart = () => (
    <div className="bg-white p-6 rounded-2xl shadow">
        <h3 className="font-semibold mb-4">Power Consumption & Savings</h3>
        <div style={{ width: '100%', height: 300 }}>
            <ResponsiveContainer>
                <AreaChart data={data}>
                    <defs>
                        <linearGradient id="colorConsumption" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor="#f472b6" stopOpacity={0.8}/>
                            <stop offset="95%" stopColor="#f472b6" stopOpacity={0}/>
                        </linearGradient>
                        <linearGradient id="colorSavings" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor="#4ade80" stopOpacity={0.8}/>
                            <stop offset="95%" stopColor="#4ade80" stopOpacity={0}/>
                        </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Area type="monotone" dataKey="consumption" stroke="#ec4899" fillOpacity={1} fill="url(#colorConsumption)" />
                    <Area type="monotone" dataKey="savings" stroke="#22c55e" fillOpacity={1} fill="url(#colorSavings)" />
                </AreaChart>
            </ResponsiveContainer>
        </div>
    </div>
);

export default PowerChart;