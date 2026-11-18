import { useState } from 'react'
import './App.css'
import { Routes, Route, Link } from 'react-router';
import { HomePage } from './pages/HomePage';
import { AboutPage } from './pages/AboutPage';
import { LoginPage } from './pages/LoginPage';

function App() {
  return (
    <div className="min-h-screen flex flex-col bg-slate-50 text-slate-900 font-sans">
      {/* Pasek nawigacji */}
      <header className="sticky top-0 z-50 bg-white/80 backdrop-blur-md border-b border-slate-200">
        <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
          {/* Logo zbudowane w samym CSS */}
          <Link to="/" className="flex items-center gap-2.5 font-bold text-xl text-indigo-600">
            <span className="w-7 h-7 rounded-lg bg-indigo-600 text-white flex items-center justify-center text-sm font-extrabold">
            </span>
            <span>Profesjonalne Systemy ESG</span>
          </Link>

          <nav className="flex items-center gap-6">
            <Link to="/" className="text-sm font-medium text-slate-600 hover:text-indigo-600 transition">
              Strona główna
            </Link>
            <Link to="/o-nas" className="text-sm font-medium text-slate-600 hover:text-indigo-600 transition">
              O projekcie
            </Link>
            <Link
              to="/login"
              className="bg-indigo-600 text-white text-sm font-medium px-4 py-2 rounded-lg hover:bg-indigo-700 transition shadow-sm"
            >
              Zaloguj się
            </Link>
          </nav>
        </div>
      </header>

      {/* Główna zawartość */}
      <main className="flex-grow">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/o-nas" element={<AboutPage />} />
          <Route path="/login" element={<LoginPage />} />
        </Routes>
      </main>

      {/* Stopka */}
      <footer className="bg-white border-t border-slate-200 py-8 text-center text-sm text-slate-500">
        © {new Date().getFullYear()} Profesjonalne Systemy ESG
      </footer>
    </div>
  );
}

export default App;