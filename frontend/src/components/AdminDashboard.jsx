// src/components/AdminDashboard.jsx
import React from 'react';
import { useNavigate } from 'react-router-dom';

export default function AdminDashboard() {
  const navigate = useNavigate();

  return (
    <div style={{ padding: '20px', position: 'relative', minHeight: '100vh' }}>
      <button
        onClick={() => navigate('/')}
        style={{
          position: 'absolute',
          top: '10px',
          left: '10px',
          padding: '8px 12px',
          cursor: 'pointer',
        }}
      >
        Powróć do kalendarza
      </button>

      <h1>Dashboard administratora</h1>
      <p>Tu możesz zarządzać rezerwacjami itp.</p>
    </div>
  );
}
