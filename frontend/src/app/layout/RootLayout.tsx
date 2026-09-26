import React from 'react';
import { Outlet } from 'react-router-dom';
import { Navbar } from '../../shared/ui/Navbar';
import { Footer } from '../../shared/ui/Footer';

export const RootLayout: React.FC = () => {
  return (
    <div className="flex flex-col min-h-screen">
      <Navbar />
      <main className="flex-1">
        <Outlet />
      </main>
      <Footer />
    </div>
  );
};
