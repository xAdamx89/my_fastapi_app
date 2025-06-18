import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

export default function AdminDashboard() {
  const navigate = useNavigate();
  const [reservations, setReservations] = useState([]);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    date: '',
  });
  const [editingId, setEditingId] = useState(null); // ID aktualnie edytowanej rezerwacji

  // Pobranie rezerwacji
  const fetchReservations = () => {
    fetch('http://localhost:8000/reservations')
      .then((res) => res.json())
      .then((data) => setReservations(data))
      .catch((err) => console.error('Błąd podczas pobierania:', err));
  };

  useEffect(() => {
    fetchReservations();
  }, []);

  // Usuwanie
  const handleDelete = (id) => {
    fetch(`http://localhost:8000/reservations/${id}`, {
      method: 'DELETE',
    })
      .then(() => setReservations((prev) => prev.filter((r) => r.id !== id)))
      .catch((err) => console.error('Błąd usuwania:', err));
  };

  // Dodawanie lub edycja
  const handleSubmit = (e) => {
    e.preventDefault();

    if (editingId) {
      // Edytowanie istniejącej rezerwacji
      fetch(`http://localhost:8000/reservations/${editingId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      })
        .then(() => {
          fetchReservations();
          setEditingId(null);
          setFormData({ name: '', email: '', date: '' });
        })
        .catch((err) => console.error('Błąd edycji:', err));
    } else {
      // Dodawanie nowej rezerwacji
      fetch('http://localhost:8000/appointments', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      })
        .then((res) => res.json())
        .then(() => {
          fetchReservations();
          setFormData({ name: '', email: '', date: '' });
        })
        .catch((err) => console.error('Błąd dodawania:', err));
    }
  };

  const startEdit = (res) => {
    setEditingId(res.id);
    setFormData({
      name: res.name,
      email: res.email,
      date: res.date,
    });
  };

  const cancelEdit = () => {
    setEditingId(null);
    setFormData({ name: '', email: '', date: '' });
  };

  return (
    <div style={{ padding: '20px' }}>
      <button onClick={() => navigate('/')}>Powróć do kalendarza</button>

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
        <input
          type="date"
          value={formData.date}
          onChange={(e) => setFormData({ ...formData, date: e.target.value })}
          required
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
            <th>Data</th>
            <th>Akcje</th>
          </tr>
        </thead>
        <tbody>
          {reservations.map((res) => (
            <tr key={res.id}>
              <td>{res.name}</td>
              <td>{res.email}</td>
              <td>{res.date}</td>
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
