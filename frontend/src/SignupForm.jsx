import React, { useState } from 'react';

export default function SignupForm() {
  const [formData, setFormData] = useState({
    ragione_sociale: '',
    partita_iva: '',
    codice_fiscale: '',
    settore: '',
    data_creazione: '',
    sede: '',
    codice_ateco: '',
    tipo: '',
    indirizzo_email: '',
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
      const response = await fetch('http://127.0.0.1:8000/signup', {   // L'INDIRIZZO DEVE CORRISPONDERE ALLA RIGA "@app.post" DELLA CORRISPONDENTE AZIONE NEL FILE MAIN.PY NEL BACKEND!
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (!response.ok) {
        // FastAPI restituisce gli errori dentro 'detail'
        throw new Error(data.detail || 'Errore durante la registrazione');
      }

      setMessage(data.message);
      setFormData({
        ragione_sociale: '',
        partita_iva: '',
        codice_fiscale: '',
        settore: '',
        data_creazione: '',
        sede: '',
        codice_ateco: '',
        tipo: '',
        indirizzo_email: '',
        password: ''
      }); // Reset del form

    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div style={{ maxWidth: '400px', margin: '2rem auto' }}>
      <h2>Registrazione</h2>

      {message && <p style={{ color: 'green' }}>{message}</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}

      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '1rem' }}>
          <label>ragione_sociale:</label>
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
          <label>Email:</label>
          <input
            type="text"
            name="partita_iva"
            value={formData.partita_iva}
            onChange={handleChange}
            required
            style={{ width: '100%', padding: '8px' }}
          />
        </div>

        <div style={{ marginBottom: '1rem' }}>
        <label>codice_fiscale:</label>
        <input
        type="text"
        name="codice_fiscale"
        value={formData.codice_fiscale}
        onChange={handleChange}
        required
        style={{ width: '100%', padding: '8px' }}
        />
        </div>

        <div style={{ marginBottom: '1rem' }}>
        <label>settore:</label>
        <input
        type="text"
        name="settore"
        value={formData.settore}
        onChange={handleChange}
        required
        style={{ width: '100%', padding: '8px' }}
        />
        </div>

        <div style={{ marginBottom: '1rem' }}>
        <label>data_creazione:</label>
        <input
        type="text"
        name="data_creazione"
        value={formData.data_creazione}
        onChange={handleChange}
        required
        style={{ width: '100%', padding: '8px' }}
        />
        </div>

        <div style={{ marginBottom: '1rem' }}>
        <label>sede:</label>
        <input
        type="text"
        name="sede"
        value={formData.sede}
        onChange={handleChange}
        required
        style={{ width: '100%', padding: '8px' }}
        />
        </div>

        <div style={{ marginBottom: '1rem' }}>
        <label>codice_ateco:</label>
        <input
        type="text"
        name="codice_ateco"
        value={formData.codice_ateco}
        onChange={handleChange}
        required
        style={{ width: '100%', padding: '8px' }}
        />
        </div>

        <div style={{ marginBottom: '1rem' }}>
        <label>tipo:</label>
        <input
        type="text"
        name="tipo"
        value={formData.tipo}
        onChange={handleChange}
        required
        style={{ width: '100%', padding: '8px' }}
        />
        </div>

        <div style={{ marginBottom: '1rem' }}>
        <label>indirizzo_email:</label>
        <input
        type="text"
        name="indirizzo_email"
        value={formData.indirizzo_email}
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
          Registrati
        </button>
      </form>
    </div>
  );
}
