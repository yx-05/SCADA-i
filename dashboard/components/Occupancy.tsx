// file: components/Occupancy.tsx
'use client';

import { User } from 'lucide-react';
import clsx from 'clsx';

type SeatStatus = 'Available' | 'Occupied' | 'Seat Hogging';

type Seat = {
  id: string;
  row: 'A' | 'B' | 'C' | 'D';
  status: SeatStatus;
  position: { top: string; left: string };
};

type Table = {
  id: number;
  position: { top: string; left: string };
  rotation: number;
  size: { width: string; height: string };
};


const seats: Seat[] = [
  // Row A
  { id: 'A01', row: 'A', status: 'Available', position: { top: '54%', left: '9%' } },
  { id: 'A02', row: 'A', status: 'Seat Hogging', position: { top: '43%', left: '13%' } },
  { id: 'A03', row: 'A', status: 'Occupied', position: { top: '32%', left: '17%' } }, 
  { id: 'A04', row: 'A', status: 'Available', position: { top: '20%', left: '21%' } }, 

  // Row B
  { id: 'B01', row: 'B', status: 'Available', position: { top: '60%', left: '25%' } },
  { id: 'B02', row: 'B', status: 'Occupied', position: { top: '71%', left: '30%' } },
  { id: 'B03', row: 'B', status: 'Available', position: { top: '92%', left: '31%' } },
  { id: 'B04', row: 'B', status: 'Occupied', position: { top: '80%', left: '73%' } },
  { id: 'B05', row: 'B', status: 'Available', position: { top: '67%', left: '77%' } },
  
  // Row C
  { id: 'C01', row: 'C', status: 'Available', position: { top: '78%', left: '44%' } },
  { id: 'C02', row: 'C', status: 'Occupied', position: { top: '60%', left: '44%' } },
  { id: 'C03', row: 'C', status: 'Available', position: { top: '45%', left: '48%' } },
  { id: 'C04', row: 'C', status: 'Available', position: { top: '76%', left: '49%' } },
  { id: 'C05', row: 'C', status: 'Seat Hogging', position: { top: '60%', left: '53%' } },

  // Row D
  { id: 'D01', row: 'D', status: 'Available', position: { top: '20%', left: '48%' } },
  { id: 'D02', row: 'D', status: 'Occupied', position: { top: '20%', left: '53%' } },
  { id: 'D03', row: 'D', status: 'Available', position: { top: '25%', left: '73%' } },
  { id: 'D04', row: 'D', status: 'Occupied', position: { top: '38%', left: '77%' } },
];

const tables: Table[] = [
  // Row A
  { id: 1, position: { top: '44%', left: '7%' }, rotation: -40, size: { width: '4%', height: '10%' } },
  { id: 2, position: { top: '32%', left: '11%' }, rotation: -40, size: { width: '4%', height: '10%' } },
  { id: 3, position: { top: '20%', left: '15%' }, rotation: -40, size: { width: '4%', height: '10%' } },
  { id: 4, position: { top: '9%', left: '19%' }, rotation: -40, size: { width: '4%', height: '10%' } }, 

  // Row B
  { id: 5, position: { top: '74%', left: '25%' }, rotation: -142, size: { width: '11%', height: '10%' } },
  { id: 11, position: { top: '89%', left: '76%' }, rotation: -225, size: { width: '4%', height: '10%' } },
  { id: 12, position: { top: '75%', left: '80%' }, rotation: -225, size: { width: '4%', height: '10%' } }, 

  //Row C
  { id: 6, position: { top: '58%', left: '49%' }, rotation: -48, size: { width: '11%', height: '10%' } },

  //Row D
  { id: 7, position: { top: '7%', left: '48%' }, rotation: 0, size: { width: '4%', height: '10%' } },
  { id: 8, position: { top: '7%', left: '53%' }, rotation: 0, size: { width: '4%', height: '10%' } }, 
  { id: 9, position: { top: '14%', left: '75%' }, rotation: 40, size: { width: '4%', height: '10%' } },
  { id: 10, position: { top: '26%', left: '79%' }, rotation: 40, size: { width: '4%', height: '10%' } }, 
];

// Function to determine the color of the progress bar
const getProgressColor = (percentage: number) => {
  if (percentage <= 50) {
    return 'bg-green-500'; // Low Occupancy
  } else if (percentage <= 80) {
    return 'bg-yellow-500'; // Medium Occupancy / Warning
  } else {
    return 'bg-red-500'; // High Occupancy / Critical
  }
};

// Reusable component for the status icons
const StatusIcon = ({ status }: { status: SeatStatus }) => (
  <div
    className={clsx(
      'w-8 h-8 rounded-full flex items-center justify-center border-2',
      {
        // Available: White fill, gray border
        'bg-white border-gray-400 text-gray-400': status === 'Available',
        // Occupied: Dark gray/black fill, white icon
        'bg-gray-800 border-gray-800 text-white': status === 'Occupied',
        // Seat Hogging: Red fill, white icon
        'bg-red-500 border-red-700 text-white': status === 'Seat Hogging',
      }
    )}
  >
    {status !== 'Available' && <User size={20} />}
  </div>
);

// Reusable component for the progress bars
const RowProgress = ({ title, stats }: { title: string; stats: { occupied: number; total: number; percentage: number } }) => {
  const colorClass = getProgressColor(stats.percentage);

  return (
    <div className="bg-white p-3 rounded-lg shadow-sm">
      <div className="flex justify-between items-center mb-1">
        <span className="font-bold text-gray-700">{title}</span>
        <span className="text-sm text-gray-500">{stats.occupied}/{stats.total}</span>
      </div>
      <div className="w-full bg-gray-200 rounded-full h-2">
        <div
          className={clsx('h-2 rounded-full', colorClass)}
          style={{ width: `${stats.percentage}%` }}
        ></div>
      </div>
      <div className="text-right text-sm text-gray-600 mt-1">
        {stats.percentage.toFixed(0)}% occupied
      </div>
    </div>
  );
};

export default function OccupancyDisplay() {
  // --- AUTOMATIC CALCULATION LOGIC ---
  const rowStats = seats.reduce(
    (acc, seat) => {
      const rowKey = `row${seat.row}`;
      // Initialize if not present (only needed if rows were dynamic)
      if (!acc[rowKey]) acc[rowKey] = { total: 0, occupied: 0, percentage: 0 }; 

      acc[rowKey].total += 1;
      if (seat.status !== 'Available') {
        acc[rowKey].occupied += 1;
      }
      return acc;
    },
    {
      rowA: { total: 0, occupied: 0, percentage: 0 },
      rowB: { total: 0, occupied: 0, percentage: 0 },
      rowC: { total: 0, occupied: 0, percentage: 0 },
      rowD: { total: 0, occupied: 0, percentage: 0 },
    }
  );

  // Calculate percentages after counting totals
  const finalStats = Object.fromEntries(
    Object.entries(rowStats).map(([key, row]) => [
      key,
      {
        ...row,
        percentage: row.total > 0 ? (row.occupied / row.total) * 100 : 0,
      },
    ])
  );


  return (
    // Main card container
    <div className="bg-white p-4 sm:p-6 rounded-2xl shadow-md col-span-1 lg:col-span-2">
      <h3 className="font-semibold text-gray-800 text-xl mb-4 text-center">Occupancy (Digital Twin)</h3>
      
      {/* Map Area */}
      <div className className="relative w-full h-[400px] bg-gray-50 rounded-lg p-4 mb-6 border border-gray-200">
        
        {/* Render Tables */}
        {tables.map(table => (
          <div
            key={table.id}
            className="absolute bg-gray-200 flex items-center justify-center text-gray-500 text-sm font-semibold rounded"
            style={{
              top: table.position.top,
              left: table.position.left,
              width: table.size.width,
              height: table.size.height,
              transform: `translate(-50%, -50%) rotate(${table.rotation}deg)`,
            }}
          >
            TABLE
          </div>
        ))}
        
        {/* Render Seats */}
        {seats.map(seat => (
          <div
            key={`${seat.id}-${seat.position.left}-${seat.position.top}`}
            className="absolute flex flex-col items-center"
            style={{
              top: seat.position.top,
              left: seat.position.left,
              transform: 'translate(-50%, -50%)',
            }}
          >
            <StatusIcon status={seat.status} />
            <span className="mt-1 text-xs font-medium text-gray-600">{seat.id}</span>
          </div>
        ))}

        {/* Legend */}
        <div className="absolute bottom-4 left-1/2 -translate-x-1/2 flex items-center space-x-4 bg-white p-3 rounded-lg shadow-sm border border-gray-200">
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 rounded-full bg-white border-2 border-gray-400"></div>
            <span className="text-xs font-medium text-gray-600">Available</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 rounded-full bg-gray-800 border-2 border-gray-800"></div>
            <span className="text-xs font-medium text-gray-600">Occupied</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 rounded-full bg-red-500 border-2 border-red-700"></div>
            <span className="text-xs font-medium text-gray-600">Seat hogging</span>
          </div>
        </div>
      </div>

      {/* Progress Bars */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <RowProgress title="Row A" stats={finalStats.rowA} />
        <RowProgress title="Row B" stats={finalStats.rowB} />
        <RowProgress title="Row C" stats={finalStats.rowC} />
        <RowProgress title="Row D" stats={finalStats.rowD} />
      </div>
    </div>
  );
}