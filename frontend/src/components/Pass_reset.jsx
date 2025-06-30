import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import './AdminPanel.css';

export default function PassReset() {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const handleReset = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");

    if (!username || !newPassword) {
      setError("Wszystkie pola są wymagane.");
      return;
    }

    try {
      const response = await fetch("http://46.205.243.253:8000/pass_reset", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: username,
          new_password: newPassword,
        }),
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.detail || "Błąd podczas resetu hasła");
      }

      setSuccess("Hasło zostało zresetowane pomyślnie.");
      // Opcjonalnie: po chwili przekieruj na stronę logowania
      setTimeout(() => {
        navigate("/login");
      }, 2000);

    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="container">
      <div className="column">

      </div>
      <div className="center-column" style={{width: '1100px'}}>
        <div className="centered">
          <h2>Resetowanie hasła</h2>
          <form onSubmit={handleReset}>
            <div className="input-group">
              <input
                type="text"
                placeholder="Nazwa użytkownika"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />
            </div>
            <div className="input-group">
              <input
                type="password"
                placeholder="Nowe hasło"
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                required
              />
            </div>
            <button type="submit" className="login-button">Zresetuj hasło</button>
          </form>
          {error && <p style={{ color: "red" }}>{error}</p>}
          {success && <p style={{ color: "green" }}>{success}</p>}
          <button type="button" className="login-button" onClick={() => navigate("/")}>
            Powrót do logowania
          </button>
        </div>
        <div className="column">

      </div>
      </div>
    </div>
  );
}
