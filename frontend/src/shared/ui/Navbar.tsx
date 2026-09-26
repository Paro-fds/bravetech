import React from 'react';
import { GraduationCap, ArrowUpRight } from 'lucide-react';
import { Link } from 'react-router-dom';

export const Navbar: React.FC = () => {
  return (
    <header className="sticky top-0 z-50 glass-nav">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between">
        {/* Brand */}
        <Link to="/" className="flex items-center gap-3.5 group">
          <div className="w-11 h-11 rounded-xl bg-gradient-to-tr from-blue-900 to-blue-600 flex items-center justify-center text-white shadow-md shadow-blue-900/20 group-hover:scale-105 transition-transform">
            <GraduationCap className="w-6 h-6" />
          </div>
          <div className="flex flex-col">
            <span className="font-extrabold text-lg sm:text-xl tracking-tight text-slate-900">
              FDS <span className="text-blue-600">PORTAIL</span>
            </span>
            <span className="text-[11px] font-semibold text-slate-500 uppercase tracking-widest">
              Faculté des Sciences · UEH
            </span>
          </div>
        </Link>

        {/* Navigation links */}
        <nav className="hidden md:flex items-center gap-8 text-sm font-medium text-slate-600">
          <Link to="/" className="text-blue-600 font-semibold hover:text-blue-700 transition-colors">
            Cursus & Formations
          </Link>
          <a href="#processus" className="hover:text-slate-900 transition-colors">
            Comment Postuler
          </a>
          <a href="#admission" className="hover:text-slate-900 transition-colors">
            Conditions d'admission
          </a>
          <a href="#contact" className="hover:text-slate-900 transition-colors">
            Contact & Secrétariat
          </a>
        </nav>

        {/* Action button */}
        <div className="flex items-center gap-3">
          <Link
            to="/#catalogue"
            className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-semibold text-sm shadow-md shadow-blue-600/25 transition-all hover:shadow-lg hover:shadow-blue-600/35"
          >
            <span>Explorer les filières</span>
            <ArrowUpRight className="w-4 h-4" />
          </Link>
        </div>
      </div>
    </header>
  );
};
