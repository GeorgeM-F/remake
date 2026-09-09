import React, { useState } from 'react';

export default function LoginForm() {
  const [formData, setFormData] = useState({
    nome: '',
    password: '',
  });
  const [message, setMessage] = useState(null);
  const [error, setError] = useState(null);
  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };
  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage(null);
    setError(null);

    try {
      const response = await fetch('http://127.0.0.1:8000/login', {   // L'INDIRIZZO DEVE CORRISPONDERE ALLA RIGA "@app.post" DELLA CORRISPONDENTE AZIONE NEL FILE MAIN.PY NEL BACKEND!
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Credenziali non valide');
      }
      // AGGIUNTA TOKEN (SE IL BACKEND NE RESTITUISCE UNO, ES: JWT)
      //if (data.access_token) {
      //  localStorage.setItem('token', data.access_token);
      //}
      setMessage(data.message);
      setFormData({
        nome: '',
        password: ''
      });

    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div style={{ maxWidth: '400px', margin: '2rem auto' }}>
      <h2>Accesso</h2>

      {message && <p style={{ color: 'green' }}>{message}</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}

      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '1rem' }}>
          <label>Ragione sociale:</label>
          <input
            type="text"
            name="ragione_sociale"
            value={formData.ragione_sociale}
            onChange={handleChange}
            required
            style={{ width: '100%', padding: '8px' }}
          />
        </div>

        <div style={{ marginBottom: '1rem' }}>
          <label>Password:</label>
          <input
            type="text"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
            style={{ width: '100%', padding: '8px' }}
          />
        </div>

        <button type="submit" style={{ padding: '10px 20px', cursor: 'pointer' }}>
          Accedi
        </button>
      </form>
    </div>
  );
}
