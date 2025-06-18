import React, { useEffect, useState, useRef } from 'react';
import FullCalendar from '@fullcalendar/react';
import dayGridPlugin from '@fullcalendar/daygrid';
import timeGridPlugin from '@fullcalendar/timegrid';
import interactionPlugin from '@fullcalendar/interaction';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

export default function CalendarView() {
  const [events, setEvents] = useState([]);
  const [currentView, setCurrentView] = useState('dayGridMonth');
  const navigate = useNavigate();
  const calendarRef = useRef(null);

  useEffect(() => {
    axios.get('http://localhost:8000/appointments')
      .then(res => {
        const formattedEvents = res.data.map(event => ({
          title: 'Spotkanie - termin zajęty',
          start: event.start,    // start datetime from backend
          end: event.koniec,     // end datetime from backend
          allDay: false,         // zakładam, że w backend masz pełne daty
        }));
        setEvents(formattedEvents);
      })
      .catch(err => console.error('Błąd podczas pobierania danych:', err));
  }, []);

  const handleSelect = (info) => {
    // Sprawdzenie czy termin jest zajęty - możesz rozbudować o sprawdzanie zakresów godzin
    const isTaken = events.some(event =>
      (new Date(info.start) < new Date(event.end)) && (new Date(info.end) > new Date(event.start))
    );
    if (isTaken) {
      alert("Ten termin jest już zajęty. Wybierz inny.");
      return;
    }

    const name = prompt("Podaj swoje imię:");
    if (!name) return alert("Imię jest wymagane.");

    const email = prompt("Podaj swój email:");
    if (!email || !email.includes('@')) return alert("Podaj poprawny email.");

    axios.post('http://localhost:8000/appointments', {
      name,
      email,
      start: info.startStr,
      koniec: info.endStr,
    })
    .then(() => {
      setEvents(prevEvents => [
        ...prevEvents,
        {
          title: 'Spotkanie - termin zajęty',
          start: info.start,
          end: info.end,
          allDay: currentView === 'dayGridMonth',  // jeśli widok month, to allDay: true
        }
      ]);
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

  const handleViewDidMount = (arg) => {
    setCurrentView(arg.view.type);
  };

  return (
    <div>
      <button onClick={() => navigate('/admin')} style={{ padding: "8px 12px" }}>
        Zaloguj się do panelu administratora
      </button>
      <FullCalendar
        ref={calendarRef}
        plugins={[dayGridPlugin, timeGridPlugin, interactionPlugin]}
        initialView="dayGridMonth"
        selectable={true}
        select={handleSelect}
        headerToolbar={{
          left: 'prev,next today',
          center: 'title',
          right: 'dayGridMonth,timeGridWeek,timeGridDay',
        }}
        events={events}
        height="auto"
        viewDidMount={handleViewDidMount}
      />
    </div>
  );
}
