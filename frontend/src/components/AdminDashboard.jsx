import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

export default function AdminDashboard() {
  const navigate = useNavigate();
  const [reservations, setReservations] = useState([]);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    start: '',
    koniec: '',
    note: '',
  });
  const [editingId, setEditingId] = useState(null);

  const fetchReservations = () => {
    fetch('http://localhost:8000/reservations')
      .then((res) => res.json())
      .then((data) => setReservations(data))
      .catch((err) => console.error('Błąd podczas pobierania:', err));
  };

  useEffect(() => {
    fetchReservations();
  }, []);

  const handleDelete = (id) => {
    fetch(`http://localhost:8000/reservations/${id}`, {
      method: 'DELETE',
    })
      .then(() => setReservations((prev) => prev.filter((r) => r.id !== id)))
      .catch((err) => console.error('Błąd usuwania:', err));
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    const payload = {
      ...formData,
      allDay: false, // lub true, jeśli potrzebujesz — dopóki nie ma inputu, ustaw ręcznie
    };

    const url = editingId
      ? `http://localhost:8000/reservations/${editingId}`
      : 'http://localhost:8000/appointments';
    const method = editingId ? 'PUT' : 'POST';

    fetch(url, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    })
      .then((res) => res.json())
      .then(() => {
        fetchReservations();
        setEditingId(null);
        setFormData({ name: '', email: '', start: '', koniec: '', note: '' });
      })
      .catch((err) => console.error('Błąd dodawania/edycji:', err));
  };

  const toLocalDateTime = (isoString) => {
    if (!isoString) return '';
    const dt = new Date(isoString);
    const off = dt.getTimezoneOffset();
    const localDate = new Date(dt.getTime() - off * 60000);
    return localDate.toISOString().slice(0, 16);
  };

  const startEdit = (res) => {
    setEditingId(res.id);
    setFormData({
      name: res.name,
      email: res.email,
      start: toLocalDateTime(res.start),
      koniec: toLocalDateTime(res.koniec),
      note: res.note || '',
    });
  };

  const cancelEdit = () => {
    setEditingId(null);
    setFormData({ name: '', email: '', start: '', koniec: '', note: '' });
  };

  return (
    <div style={{ padding: '20px' }}>
      <button onClick={() => navigate('/calendar')}>Powróć do kalendarza</button>

      <h1>Dashboard administratora</h1>

      <h2>{editingId ? 'Edytuj rezerwację' : 'Dodaj rezerwację'}</h2>
      <form onSubmit={handleSubmit} style={{ marginBottom: '20px' }}>
        <input
          type="text"
          placeholder="Imię i nazwisko"
          value={formData.name}
          onChange={(e) => setFormData({ ...formData, name: e.target.value })}
          required
        />
        <input
          type="email"
          placeholder="Email"
          value={formData.email}
          onChange={(e) => setFormData({ ...formData, email: e.target.value })}
          required
        />
        <label>
          Start:
          <input
            type="datetime-local"
            value={formData.start}
            onChange={(e) => setFormData({ ...formData, start: e.target.value })}
            required
          />
        </label>
        <label>
          Koniec:
          <input
            type="datetime-local"
            value={formData.koniec}
            onChange={(e) => setFormData({ ...formData, koniec: e.target.value })}
            required
          />
        </label>
        <input
         style={{position: "relative", top: "4px", marginBottom: "10px"}}
          type="text"
          placeholder="Notatka"
          value={formData.note}
          onChange={(e) => setFormData({ ...formData, note: e.target.value })}
        />
        <button type="submit">{editingId ? 'Zapisz zmiany' : 'Dodaj'}</button>
        {editingId && (
          <button type="button" onClick={cancelEdit} style={{ marginLeft: '10px' }}>
            Anuluj
          </button>
        )}
      </form>

      <h2>Lista rezerwacji</h2>
      <table border="1" cellPadding="8" style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr>
            <th>Imię i nazwisko</th>
            <th>Email</th>
            <th>Start</th>
            <th>Koniec</th>
            <th>Notatka</th>
            <th>Akcje</th>
          </tr>
        </thead>
        <tbody>
          {reservations.map((res) => (
            <tr key={res.id}>
              <td>{res.name}</td>
              <td>{res.email}</td>
              <td>{new Date(res.start).toLocaleString()}</td>
              <td>{new Date(res.koniec).toLocaleString()}</td>
              <td>{res.note || '-'}</td>
              <td>
                <button onClick={() => startEdit(res)}>Edytuj</button>{' '}
                <button onClick={() => handleDelete(res.id)}>Usuń</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}