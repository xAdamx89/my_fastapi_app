import { useNavigate } from 'react-router-dom';
import { useState } from 'react';
import './AdminPanel.css';

export default function AdminPanel() {
  const navigate = useNavigate();
  const [login, setLogin] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = (e) => {
    e.preventDefault();

    // Prosty przykład: sprawdzanie loginu i hasła na sztywno
    if (login === 'admin' && password === 'haslo123') {
      navigate('/admin/dashboard');
    } else {
      alert('Nieprawidłowy login lub hasło.');
    }
  };

  return (
    <div className="column">
      <button className="to-left" onClick={() => navigate('/')}>
        Powróć do kalendarza
      </button>
      <div>
        <div className="centered">
          <h2>Logowanie do panelu admina</h2>
          <form onSubmit={handleLogin}>
            <div style={{ marginBottom: '10px' }}>
              <input
                type="text"
                placeholder="Login"
                value={login}
                onChange={(e) => setLogin(e.target.value)}
                style={{ width: '100%', padding: '8px' }}
                required
              />
            </div>
            <div style={{ marginBottom: '10px' }}>
              <input
                type="password"
                placeholder="Hasło"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                style={{ width: '100%', padding: '8px' }}
                required
              />
            </div>
            <button type="submit" style={{ padding: '8px 16px' }}>
              Zaloguj
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
