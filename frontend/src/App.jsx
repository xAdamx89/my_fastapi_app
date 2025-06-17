import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import CalendarView from './components/CalendarView';

function AdminPanel() {
  return (
    <div>
      <h1>Panel Administratora</h1>
      <p>Tu będzie Twój panel admina.</p>
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<CalendarView />} />
        <Route path="/admin" element={<AdminPanel />} />
      </Routes>
    </BrowserRouter>
  );
}
