import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import './AdminPanel.css'

export default function Login() {
  const navigate = useNavigate();
  const [login, setLogin] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");

    // Prosta walidacja dla user/user bez backendu
    if (login === "user" && password === "user") {
        // Symulacja zapisu tokenu (np. "dummy-token")
        localStorage.setItem("access_token", "dummy-token-user");
        navigate("/calendar");
        return;
    }

    try {
        const response = await fetch("http://localhost:8000/token", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: new URLSearchParams({
            username: login,
            password: password,
        }),
        });

        if (!response.ok) {
        throw new Error("Nieprawidłowy login lub hasło");
        }

        const data = await response.json();
        localStorage.setItem("access_token", data.access_token);
        navigate("/calendar");
    } catch (err) {
        setError(err.message);
    }
};

  return (
    <div className="container">
        <div className="column">
            <button type="button" className="login-button" onClick={() => navigate("/rejestracja")}>
            Zarejestruj się
            </button>
        </div>

        <div className="column center-column">
        <div className="centered">
            <h2>Logowanie do kalendarza</h2>
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
            <button type="submit" className="login-button">Zaloguj</button>
            </form>
            {error && <p style={{ color: "red" }}>{error}</p>}
        </div>
        </div>
        <div className="column"></div>
    </div>
);
}