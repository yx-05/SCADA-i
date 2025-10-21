// app/dashboard/page.tsx
import React from 'react';
import Header from '@/components/Header';
import StatCards from '@/components/StatCards'; 
import Charts from '@/components/Charts';
import Occupancy from '@/components/Occupancy';
import Controls from '@/components/Controls';
import AiActions from '@/components/AiActions';
import DeviceOverview from '@/components/DeviceOverview';
import UserFeedback from '@/components/UserFeedback';


// --- MAIN DASHBOARD COMPONENT (Server Component) ---
export default async function DashboardPage() {

    return (
        <div className="min-h-screen bg-gray-50 text-gray-800">
            <Header />
            <main className="p-4 sm:p-6 lg:p-8 space-y-6">
                
                {/* 1. Top 4 stat cards - PASS LIVE DATA */}
                <StatCards />

                {/* 2. The two main charts - PASS LIVE DATA */}
                <Charts />

                {/* 3. Occupancy Grid (Digital Twin) - PASS LIVE DEVICE ARRAY */}
                <Occupancy />
                
                {/* 4. Live user feedback */}
                <UserFeedback ></UserFeedback>

                {/* Controls and AI Actions side-by-side (Data connection for these is typically separate) */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    <Controls />
                    <AiActions />
                </div>

                {/* Final Device Bar Chart - PASS LIVE DEVICE ARRAY */}
                <DeviceOverview />
            </main>
        </div>
    );
}