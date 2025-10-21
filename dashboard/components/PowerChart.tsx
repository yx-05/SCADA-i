// components/PowerChart.tsx
"use client";

import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';
import { useEffect, useState } from 'react';


// const data = [
//   { name: '0:00', consumption: 400, savings: 240 },
//   { name: '4:00', consumption: 300, savings: 139 },
//   { name: '8:00', consumption: 450, savings: 580 },
//   { name: '12:00', consumption: 680, savings: 390 },
//   { name: '16:00', consumption: 720, savings: 480 },
//   { name: '20:00', consumption: 500, savings: 380 },
// ];

// Define the shape of each data row
interface PowerData {
    name: string;          // formatted time string (e.g. '08:30')
    consumption: number;   // total power usage
    savings: number;       // (placeholder or calculated if needed)
}

interface ApiPowerRow {
    timestamp: string;
    power_usage: number;
    // Add any other fields that come from the API
}

const PowerChart = () => {
    const [data, setData] = useState<PowerData[]>([]);


    useEffect(() => {
        const fetchData = async () => {
            try {
                const res = await fetch("/api/data?hours=3"); // query for last 3 hours
                if (!res.ok) throw new Error("Failed to fetch");
                const rows = await res.json();

                // Transform DB rows into chart-friendly data
                const formatted: PowerData[] = rows.map((row: ApiPowerRow) => ({
                    name: new Date(row.timestamp).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
                    consumption: row.power_usage,
                    savings: Math.max(0, 200 - row.power_usage) // placeholder
                }));

                setData(formatted);
            } catch (err) {
                console.error("Error fetching power data:", err);
            }
        };

        fetchData();
        const interval = setInterval(fetchData, 10000); // auto-update every 10s
        return () => clearInterval(interval);
    }, []);


    return (
        <div className="bg-white p-6 rounded-2xl shadow">
            <h3 className="font-semibold mb-4">Power Consumption & Savings</h3>
            <div style={{ width: '100%', height: 300 }}>
                <ResponsiveContainer>
                    <AreaChart data={data}>
                        <defs>
                            <linearGradient id="colorConsumption" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="#f472b6" stopOpacity={0.8} />
                                <stop offset="95%" stopColor="#f472b6" stopOpacity={0} />
                            </linearGradient>
                            <linearGradient id="colorSavings" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="#4ade80" stopOpacity={0.8} />
                                <stop offset="95%" stopColor="#4ade80" stopOpacity={0} />
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
}

export default PowerChart;