import React, { useEffect, useState } from 'react';
import FullCalendar from '@fullcalendar/react';
import dayGridPlugin from '@fullcalendar/daygrid';
import timeGridPlugin from '@fullcalendar/timegrid';
import interactionPlugin from '@fullcalendar/interaction';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

export default function CalendarView() {
    const [events, setEvents] = useState([]);
    const navigate = useNavigate();

  useEffect(() => {
    axios.get('http://localhost:8000/appointments')
      .then(res => setEvents(res.data))
      .catch(err => console.error('Błąd podczas pobierania danych:', err));
  }, []);

  // Obsługa kliknięcia w dzień
  const handleDateClick = (info) => {
    const isTaken = events.some(event => event.date === info.dateStr);
  if (isTaken) {
    alert("Ten termin jest już zajęty. Wybierz inny.");
    return; // przerywamy dalszą obsługę kliknięcia
  }

  const name = prompt("Podaj swoje imię:");
  if (!name) {
    alert("Imię jest wymagane.");
    return; // przerwij, jeśli nie podano imienia
  }

  const email = prompt("Podaj swój email:");
  if (!email) {
    alert("Email jest wymagany.");
    return; // przerwij, jeśli nie podano emaila
  }

  // Tutaj możesz dodać prostą walidację emaila, np. regex lub includes('@')
  if (!email.includes('@')) {
    alert("Podaj poprawny email.");
    return;
  }

  // Wyślij do backendu
  axios.post('http://localhost:8000/appointments', {
    name,
    email,
    date: info.dateStr,
  })
  .catch(error => {
    if (error.response?.status === 400) {
      alert('Ten termin jest już zajęty.');
    } else {
      alert('Wystąpił błąd podczas rezerwacji.');
      console.error(error);
    }
  });
};

  return (
    <div>
      <button onClick={() => navigate('/admin')} style={{ marginBottom: '10px' }}>
        Zaloguj się do panelu administratora
      </button>
      <FullCalendar
        plugins={[dayGridPlugin, timeGridPlugin, interactionPlugin]}
        initialView="dayGridMonth"
        headerToolbar={{
          left: 'prev,next today',
          center: 'title',
          right: 'dayGridMonth,timeGridWeek,timeGridDay',
        }}
        events={events}
        dateClick={handleDateClick}
        height="auto"
      />
    </div>
  );
}
