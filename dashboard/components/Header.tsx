// components/Header.tsx
"use client";

import { Bell, User, MoreVertical, Thermometer, Clock, AlertCircle, BarChart, LogOut, Settings, UserCircle, Shield, FileLock } from 'lucide-react';
import { useState, useEffect, useRef } from 'react';
import { useClickOutside } from '@/hooks/useClickOutside';
import Link from 'next/link';
import { useMqtt } from "@/context/MqttContext";

const notifications = [
    { icon: AlertCircle, text: 'Carbon level is high in Row D.', time: '2 mins ago', color: 'text-red-500' },
    { icon: BarChart, text: 'Energy savings report for today is available.', time: '1 hr ago', color: 'text-green-500' },
    { icon: Settings, text: 'A new device "Smart Light 12" was added.', time: '3 hrs ago', color: 'text-blue-500' },
];

const Header = () => {
  const [currentTime, setCurrentTime] = useState('');
  const [isNotificationsOpen, setIsNotificationsOpen] = useState(false);
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);

  const notificationsRef = useRef<HTMLDivElement>(null);
  const settingsRef = useRef<HTMLDivElement>(null);

  const { sensorData } = useMqtt();

  useClickOutside(notificationsRef, () => setIsNotificationsOpen(false));
  useClickOutside(settingsRef, () => setIsSettingsOpen(false));

  useEffect(() => {
    const updateTime = () => {
      setCurrentTime(new Date().toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' }));
    };
    updateTime();
    const intervalId = setInterval(updateTime, 1000);
    return () => clearInterval(intervalId);
  }, []);

  return (
    <header className="flex items-center justify-between p-4 bg-white border-b relative">
      <div className="flex items-center space-x-4">
        <div className="flex items-center space-x-2 text-gray-600"><Clock size={20} /><span className="font-medium">{currentTime || '...'}</span></div>
        <div className="flex items-center space-x-2 text-gray-600"><Thermometer size={20} /><span className="font-medium">{sensorData?.temperature ?? "No data yet..."}</span></div>
      </div>
      <div className="text-center">
        <h1 className="text-xl font-bold">University Hardware Control Dashboard</h1>
        <p className="text-sm text-gray-500">Real-time monitoring and intelligent control system</p>
      </div>
      <div className="flex items-center space-x-4">
        <div className="relative">
          <button onClick={() => setIsNotificationsOpen(!isNotificationsOpen)} className="relative">
            <Bell size={20} />
            <span className="absolute -top-1 -right-1 flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-red-500"></span>
            </span>
          </button>
          {isNotificationsOpen && (
            <div ref={notificationsRef} className="absolute top-10 right-0 w-80 bg-white rounded-lg shadow-xl border z-10">
              <div className="p-3 border-b font-semibold text-sm">Notifications</div>
              <div className="flex flex-col">
                {notifications.map((item, index) => (
                  <div key={index} className="flex items-start gap-3 p-3 hover:bg-gray-50 border-b">
                    <item.icon className={`${item.color} mt-1 flex-shrink-0`} size={20} />
                    <div>
                      <p className="text-sm">{item.text}</p>
                      <p className="text-xs text-gray-400 mt-1">{item.time}</p>
                    </div>
                  </div>
                ))}
              </div>
              <div className="p-2 text-center text-sm text-blue-600 hover:bg-gray-50 cursor-pointer">
                View all notifications
              </div>
            </div>
          )}
        </div>
        <div className="flex items-center space-x-2">
            <span className="font-medium">User</span>
            {/* This new div creates the circular border */}
            <div className="h-8 w-8 rounded-full border border-gray-300 flex items-center justify-center">
                <User size={18} className="text-gray-600" />
            </div>
        </div>
        <div className="relative">
          <button onClick={() => setIsSettingsOpen(!isSettingsOpen)}>
            <MoreVertical size={20} />
          </button>
          {isSettingsOpen && (
             <div ref={settingsRef} className="absolute top-10 right-0 w-56 bg-white rounded-lg shadow-xl border z-10">
                <ul className="py-1">
                    <li><Link href="#" className="flex items-center gap-3 px-4 py-2 text-sm hover:bg-gray-100"><UserCircle size={16} /> Profile</Link></li>
                    <li><Link href="#" className="flex items-center gap-3 px-4 py-2 text-sm hover:bg-gray-100"><Shield size={16} /> Security</Link></li>
                    <li><Link href="#" className="flex items-center gap-3 px-4 py-2 text-sm hover:bg-gray-100"><FileLock size={16} /> Data & Privacy</Link></li>
                    <hr className="my-1"/>
                    <li><Link href="/" className="flex items-center gap-3 px-4 py-2 text-sm text-red-600 hover:bg-red-50"><LogOut size={16} /> Log Out</Link></li>
                </ul>
             </div>
          )}
        </div>
      </div>
    </header>
  );
};

export default Header;