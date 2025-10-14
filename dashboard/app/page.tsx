// app/page.tsx

"use client";

import Image from 'next/image';
import { useRouter } from 'next/navigation';
import React from 'react';

export default function LoginPage() {
  const router = useRouter(); 

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault(); // This stops the page from doing a full reload.

    router.push('/dashboard'); 
  };

  return (
    <main className="flex items-center justify-center min-h-screen">
      <div className="w-full max-w-md mx-auto">
        <h1 className="text-5xl font-bold text-white text-center mb-8">
          Login
        </h1>
        <div className="bg-white/10 backdrop-blur-lg rounded-2xl shadow-xl p-8 space-y-6">
          <div className="flex flex-col items-center space-y-2 mb-6">
              <Image 
                src="/logo.png"
                alt="Bugsolver Logo"
                width={242}
                height={158}
                className="object-contain"
              />
            </div>
          
          {/* The form's onSubmit event triggers our handleLogin function */}
          <form onSubmit={handleLogin} className="space-y-6">
            <div>
              <input 
                type="email"
                placeholder="Email"
                className="w-full bg-white/20 border border-white/30 rounded-lg py-3 px-4 text-white placeholder-white-300 focus:outline-none focus:ring-2 focus:ring-white/50 transition duration-300"
                required
              />
            </div>
            <div>
              <input 
                type="password"
                placeholder="Password"
                className="w-full bg-white/20 border border-white/30 rounded-lg py-3 px-4 text-white placeholder-white-300 focus:outline-none focus:ring-2 focus:ring-white/50 transition duration-300"
                required
              />
            </div>
            <button
              type="submit" // This ensures the button submits the form.
              className="w-full bg-white/30 text-white font-bold py-3 rounded-lg hover:bg-white/40 transition-colors duration-300"
            >
              Log In
            </button>
          </form>
        </div>
      </div>
    </main>
  );
}