// src/components/AdminPanel.jsx
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './AdminPanel.css';

export default function AdminPanel() {
  const navigate = useNavigate();
  const [login, setLogin] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = (e) => {
    e.preventDefault();

    // Proste sprawdzenie loginu i hasła na sztywno
    if (login === 'admin' && password === 'haslo123') {
      navigate('/admin/dashboard');
    } else {
      alert('Nieprawidłowy login lub hasło.');
    }
  };

  return (
    <div className="container">
      <div className="column">
        <button className="to-left" onClick={() => navigate('/')}>
          Powróć do kalendarza
        </button>
      </div>

      <div className="column center-column">
        <div className="centered">
          <h2>Logowanie do panelu admina</h2>
          <form onSubmit={handleLogin}>
            <div className="input-group">
              <input
                type="text"
                placeholder="Login"
                value={login}
                onChange={(e) => setLogin(e.target.value)}
                required
              />
            </div>
            <div className="input-group">
              <input
                type="password"
                placeholder="Hasło"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
            <button type="submit" className="login-button">
              Zaloguj
            </button>
          </form>
        </div>
      </div>

      <div className="column"></div>
    </div>
  );
}
