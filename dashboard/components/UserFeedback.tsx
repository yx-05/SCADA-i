// components/UserFeedback.tsx

// --- FIX: This is the most important line. ---
// It tells Next.js that this is a Client Component because it uses hooks.
"use client";

import React, { useState, useEffect } from 'react';
import { Fan, AirVent, Projector, Lightbulb } from 'lucide-react';

// Define the shape of each feedback entry
interface Feedback {
  id: number;
  device: string;
  user: string;
  email: string;
  action: string;
  reason: string;
  timestamp: string;
}

// Map device names to their corresponding icons
const deviceIcons: { [key: string]: React.ReactElement } = {
  Fan: <Fan className="w-5 h-5 text-blue-500" />,
  AC: <AirVent className="w-5 h-5 text-cyan-500" />,
  Projector: <Projector className="w-5 h-5 text-purple-500" />,
  Light: <Lightbulb className="w-5 h-5 text-yellow-500" />,
};

// Helper function to get user initials
const getInitials = (name: string) => {
  if (!name || typeof name !== 'string') return '??';
  const names = name.split(' ');
  if (names.length > 1) {
    return `${names[0][0]}${names[names.length - 1][0]}`.toUpperCase();
  }
  return name.substring(0, 2).toUpperCase();
};

// Helper function to assign a consistent color based on user name
const colors = ['bg-blue-500', 'bg-green-500', 'bg-yellow-500', 'bg-red-500', 'bg-purple-500', 'bg-pink-500', 'bg-indigo-500', 'bg-teal-500'];
const getColorForUser = (name: string) => {
    if (!name) return 'bg-gray-500'; // Safeguard for undefined names
    const charCodeSum = name.split('').reduce((sum, char) => sum + char.charCodeAt(0), 0);
    return colors[charCodeSum % colors.length];
};

// Helper function to format the timestamp into a "time ago" string
const formatTimestamp = (timestamp: string) => {
    const now = new Date();
    const feedbackDate = new Date(timestamp);
    const seconds = Math.floor((now.getTime() - feedbackDate.getTime()) / 1000);

    if (isNaN(seconds) || seconds < 5) return "Just now";
    if (seconds < 60) return `${seconds}s ago`;

    const minutes = Math.floor(seconds / 60);
    if (minutes < 60) return `${minutes}m ago`;

    const hours = Math.floor(minutes / 60);
    if (hours < 24) return `${hours}h ago`;

    const days = Math.floor(hours / 24);
    return `${days}d ago`;
};

const UserFeedback: React.FC = () => {
  // State to hold the feedback data fetched from the API
  const [feedbackData, setFeedbackData] = useState<Feedback[]>([]);

  // Effect hook to fetch data when the component mounts and then poll for updates
  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await fetch("/api/feedback"); // Your API endpoint
        if (!res.ok) {
            console.error("Failed to fetch feedback data");
            return;
        }
        const textData = await res.text();

        // Parse the text data, filtering out any empty lines
        const parsedData: Feedback[] = textData
          .split('\n')
          .filter(line => line) // Safeguard: remove empty lines
          .map(line => {
            const [id, device, user, email, action, reason, timestamp] = line.split('|');
            return { id: Number(id), device, user, email, action, reason, timestamp };
          })
          .reverse(); // Show newest first

        setFeedbackData(parsedData);
      } catch (err) {
        console.error("Error fetching or parsing feedback data:", err);
      }
    };

    fetchData(); // Fetch immediately on mount
    const interval = setInterval(fetchData, 10000); // Set up polling every 10 seconds

    // Cleanup function to clear the interval when the component unmounts
    return () => clearInterval(interval);
  }, []); // Empty dependency array means this effect runs only once on mount

  return (
    <div className="bg-white p-6 rounded-2xl shadow">
      <h3 className="font-semibold text-gray-800 text-lg mb-4">User Feedback</h3>
      <div className="space-y-3 max-h-96 overflow-y-auto pr-2">
        {feedbackData.map((feedback) => (
          <div key={feedback.id} className="p-4 rounded-lg bg-gray-50 border border-gray-200 transition-all hover:shadow-md hover:border-gray-300">
            <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                    <div className="p-2 bg-white rounded-full border">
                        {deviceIcons[feedback.device] || <div className="w-5 h-5"/>}
                    </div>
                    <span className="font-semibold text-gray-800">{feedback.action}</span>
                </div>
                <span className="text-xs text-gray-500">{formatTimestamp(feedback.timestamp)}</span>
            </div>
            <div className="mt-3 flex items-start space-x-3 pl-1">
                <div className={`w-8 h-8 rounded-full ${getColorForUser(feedback.user)} text-white flex-shrink-0 flex items-center justify-center text-sm font-bold`}>
                    {getInitials(feedback.user)}
                </div>
                <div className="flex-1 pt-1">
                    <p className="text-sm text-gray-700">
                        Reported by <span className="font-medium">{feedback.user || 'Unknown'}</span>
                    </p>
                        <p className="text-sm text-gray-500 mt-1">
                            Reason: <span className="italic">&ldquo;{feedback.reason}&rdquo;</span>
                        </p>
                </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default UserFeedback;