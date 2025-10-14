// app/dashboard/page.tsx
import React from 'react';
import Header from '@/components/Header';
import StatCards from '@/components/StatCards'; 
import Charts from '@/components/Charts';
import Occupancy from '@/components/Occupancy';
import Controls from '@/components/Controls';
import AiActions from '@/components/AiActions';
import DeviceOverview from '@/components/DeviceOverview';

// --- DATA STRUCTURES ---
// Defines the shape of the data expected from your Python Flask API
interface DashboardData {
    carbonLevel: number | string;
    powerConsumption: number | string;
    occupancy: { current: number | string; total: number | string };
    energySaved: number | string;
    devices: Array<{ 
        device_id: number; 
        occupancy: number; // 0 or 1
        temperature: number; 
        power_usage: number;
    }>;
}

// --- DATA FETCHING FUNCTION ---
const API_URL = 'http://localhost:3000/api/dashboard/stats';

async function getLiveData(): Promise<DashboardData | null> {
    try {
        const res = await fetch(API_URL, {
            // Next.js specific: Re-fetch data every 5 seconds for "live" updates
            next: { revalidate: 5 } 
        });

        if (!res.ok) {
            console.error(`API fetch failed: ${res.status}`);
            return null;
        }

        return res.json();
    } catch (error) {
        // This catches errors if the Python API server isn't running
        console.error("Failed to connect to Python API (http://localhost:3000):", error);
        return null;
    }
}


// --- MAIN DASHBOARD COMPONENT (Server Component) ---
export default async function DashboardPage() {
    const data = await getLiveData();

    // Fallback if the API is down or fails to fetch
    const stats = data || {
        carbonLevel: 'N/A', 
        powerConsumption: 'N/A', 
        energySaved: 'N/A',
        occupancy: { current: 'N/A', total: 'N/A' },
        devices: [] // Ensure devices array is always present
    };
    
    // NOTE on components: You must now update your child components 
    // (StatCards, Occupancy, etc.) to accept and use the `stats` object as props.

    return (
        <div className="min-h-screen bg-gray-50 text-gray-800">
            <Header />
            <main className="p-4 sm:p-6 lg:p-8 space-y-6">
                
                {/* 1. Top 4 stat cards - PASS LIVE DATA */}
                <StatCards 
                    carbonLevel={stats.carbonLevel}
                    powerConsumption={stats.powerConsumption}
                    occupancy={stats.occupancy}
                    energySaved={stats.energySaved}
                />

                {/* 2. The two main charts - PASS LIVE DATA */}
                <Charts devices={stats.devices} />

                {/* 3. Occupancy Grid (Digital Twin) - PASS LIVE DEVICE ARRAY */}
                <Occupancy liveDevices={stats.devices} />

                {/* Controls and AI Actions side-by-side (Data connection for these is typically separate) */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    <Controls />
                    <AiActions />
                </div>

                {/* Final Device Bar Chart - PASS LIVE DEVICE ARRAY */}
                <DeviceOverview devices={stats.devices} />
                
            </main>
        </div>
    );
}