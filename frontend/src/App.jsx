// src/App.jsx
import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

import CalendarView from './components/CalendarView';
import AdminPanel from './components/AdminPanel';
import AdminDashboard from './components/AdminDashboard';
import Login from './components/login';
import Rejestracja from './components/Rejestracja';
import Pass_reset from './components/Pass_reset'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/calendar" element={<CalendarView />} />
        <Route path="/admin" element={<AdminPanel />} />
        <Route path="/admin/dashboard" element={<AdminDashboard />} />
        <Route path="/rejestracja" element={<Rejestracja />} />
        <Route path="/pass_reset" element={<Pass_reset />} />
      </Routes>
    </BrowserRouter>
  );
}
