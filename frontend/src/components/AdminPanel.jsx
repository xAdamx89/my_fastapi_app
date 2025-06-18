import { useNavigate } from 'react-router-dom';
import { useState } from 'react';
import './AdminPanel.css';

export default function AdminPanel() {
  const navigate = useNavigate();
  const [login, setLogin] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = (e) => {
    e.preventDefault();
    if (login === 'admin' && password === 'haslo123') {
      navigate('/admin/dashboard');
    } else {
      alert('Nieprawidłowy login lub hasło.');
    }
  };

  return (
    <div className="row">
      <div className="column" />
      
      <div className="column center-column">
        <button className="back-button" onClick={() => navigate('/')}>
          Powróć do kalendarza
        </button>

        <div className="login-box">
          <h2>Logowanie do panelu admina</h2>
          <form onSubmit={handleLogin}>
            <input
              type="text"
              placeholder="Login"
              value={login}
              onChange={(e) => setLogin(e.target.value)}
              required
            />
            <input
              type="password"
              placeholder="Hasło"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            <button type="submit">Zaloguj</button>
          </form>
        </div>
      </div>

      <div className="column" />
    </div>
  );
}
