import React, { useEffect, useState } from 'react';
import FullCalendar from '@fullcalendar/react';
import dayGridPlugin from '@fullcalendar/daygrid';
import timeGridPlugin from '@fullcalendar/timegrid';
import interactionPlugin from '@fullcalendar/interaction';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

export default function CalendarView() {
  const [events, setEvents] = useState([]);
  const [selection, setSelection] = useState(null);
  const [formData, setFormData] = useState({ name: '', email: '' });
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    axios.get('http://localhost:8000/appointments')
      .then(res => {
        const formattedEvents = res.data.map(event => ({
          title: 'Spotkanie - termin zajęty',
          start: event.start,
          end: event.koniec,
          allDay: false,
        }));
        setEvents(formattedEvents);
      })
      .catch(err => console.error('Błąd podczas pobierania danych:', err));
  }, []);

  const isWeekend = (date) => {
    const day = date.getDay();
    return day === 0 || day === 6;
  };

  const isWithinBusinessHours = (start, end) => {
    const startHour = start.getHours();
    const endHour = end.getHours();
    return startHour >= 8 && endHour <= 16 && start < end;
  };

  const handleSelect = (selectionInfo) => {
    const { start, end } = selectionInfo;

    if (isWeekend(start)) {
      setError("Nie można rezerwować w weekendy.");
      return;
    }

    if (!isWithinBusinessHours(start, end)) {
      setError("Rezerwacje możliwe są tylko w godzinach 8:00 - 16:00.");
      return;
    }

    const isOverlapping = events.some(event => {
      const existingStart = new Date(event.start).getTime();
      const existingEnd = new Date(event.end).getTime();
      return (start.getTime() < existingEnd && end.getTime() > existingStart);
    });

    if (isOverlapping) {
      setError("Ten przedział czasowy jest już zajęty.");
      return;
    }

    setSelection({ start, end });
    setFormData({ name: '', email: '' });
    setError('');
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const { start, end } = selection;
    const { name, email } = formData;

    if (!name.trim()) {
      setError("Imię jest wymagane.");
      return;
    }

    if (!email.includes('@')) {
      setError("Podaj poprawny email.");
      return;
    }

    axios.post('http://localhost:8000/appointments', {
      name,
      email,
      start: start.toISOString(),
      koniec: end.toISOString(),
      allDay: false,
    })
      .then(() => {
        setEvents(prevEvents => [
          ...prevEvents,
          {
            title: 'Spotkanie - termin zajęty',
            start: start.toISOString(),
            end: end.toISOString(),
            allDay: false,
          }
        ]);
        setSelection(null);
        setError('');
      })
      .catch(error => {
        if (error.response?.status === 400) {
          setError('Ten termin jest już zajęty.');
        } else {
          setError('Wystąpił błąd podczas rezerwacji.');
          console.error(error);
        }
      });
  };

  return (
    <div>
      <button onClick={() => navigate('/admin')} style={{ padding: "8px 12px" }}>
        Zaloguj się do panelu administratora
      </button>

      <FullCalendar
        plugins={[dayGridPlugin, timeGridPlugin, interactionPlugin]}
        initialView="dayGridMonth"
        selectable={true}
        selectMirror={true}
        selectLongPressDelay={1}
        select={handleSelect}
        headerToolbar={{
          left: 'prev,next today',
          center: 'title',
          right: 'dayGridMonth,timeGridWeek,timeGridDay',
        }}
        events={events}
        height="auto"
        validRange={{
          start: new Date().toISOString().slice(0, 10),
        }}
        businessHours={{
          daysOfWeek: [1, 2, 3, 4, 5],
          startTime: '08:00',
          endTime: '16:00',
        }}
        allDaySlot={false}
        slotMinTime="08:00:00"
        slotMaxTime="16:00:00"
      />

      {selection && (
        <div style={{
          position: 'fixed',
          top: 0, left: 0, right: 0, bottom: 0,
          backgroundColor: 'rgba(0,0,0,0.6)',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          zIndex: 9999
        }}>
          <form onSubmit={handleSubmit} style={{
            backgroundColor: 'rgb(53, 49, 49)',
            padding: '20px',
            borderRadius: '10px',
            minWidth: '300px',
            display: 'flex',
            flexDirection: 'column',
            gap: '10px'
          }}>
            <h3>Rezerwacja terminu</h3>
            <label>
              Imię:
              <input
                type="text"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                required
              />
            </label>
            <label>
              Email:
              <input
                type="email"
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                required
              />
            </label>
            {error && <div>{error}</div>}
            <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '10px' }}>
              <button type="button" onClick={() => setSelection(null)}>Anuluj</button>
              <button type="submit">Zarezerwuj</button>
            </div>
          </form>
        </div>
      )}
    </div>
  );
}
