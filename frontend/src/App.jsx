// src/App.jsx
import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

import CalendarView from './components/CalendarView'; // zakładam, że masz
import AdminPanel from './components/AdminPanel';
import AdminDashboard from './components/AdminDashboard';
import Login from './components/Login';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/calendar" element={<CalendarView />} />
        <Route path="/admin" element={<AdminPanel />} />
        <Route path="/admin/dashboard" element={<AdminDashboard />} />
      </Routes>
    </BrowserRouter>
  );
}
