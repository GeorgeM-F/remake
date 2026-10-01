import React, { useState } from 'react';

export default function SaverForm() {
  const [formData, setFormData] = useState({
    risposta: '',
    descrizione: '',
    autovalutazione: '',
    priorità: '',
    note: ''
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
      const response = await fetch('http://127.0.0.1:8000/saver', {   // L'INDIRIZZO DEVE CORRISPONDERE ALLA RIGA "@app.post" DELLA CORRISPONDENTE AZIONE NEL FILE MAIN.PY NEL BACKEND!
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });
      const data = await response.json();   // definisce "data" come il json di risposta
      if (!response.ok) {
        throw new Error(data.detail);   // nota: FastAPI restituisce gli errori dentro 'detail'
      }
      setMessage(data.message);
      setFormData({
        risposta: '',
        descrizione: '',
        autovalutazionee: '',
        priorità: '',
        note: ''
      }); // Reset del form
    } catch (err) {
      setError(err.message);
    }
  };



// HTML DI RISPOSTA //
  return (
    <div style={{ maxWidth: '400px', margin: '2rem auto' }}>
      <h2>Domanda n°</h2>

      {message && <p style={{ color: 'green' }}>{message}</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}

      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '1rem' }}>
        <label>Risposta:</label>
        <input type="radio" name="risposta" value={formData.risposta} onChange={handleChange} required style={{ width: '100%', padding: '8px' }}  /><label><strong>no</strong></label>
        <input type="radio" name="risposta" value={formData.risposta} onChange={handleChange} required style={{ width: '100%', padding: '8px' }}  /><label><strong>in parte</strong></label>
        <input type="radio" name="risposta" value={formData.risposta} onChange={handleChange} required style={{ width: '100%', padding: '8px' }}  /><label><strong>sì</strong></label>
        </div>

        <div style={{ marginBottom: '1rem' }}>
        <label>Descrizione delle attività attualmente implementate dall\'Organizzazione:</label>
        <input type="text" name="descrizione" value={formData.descrizione}  onChange={handleChange} required  style={{ width: '100%', padding: '8px' }} />
        </div>

        <div style={{ marginBottom: '1rem' }}>
        <label>Auto-valutazione delle attività attualmente implementate dall\'Organizzazione:</label>
        <input type="range" min="1" max="5" name="autovalutazione" value={formData.autovalutazione} onChange={handleChange} required style={{ width: '100%', padding: '8px' }} />
        </div>

        <div style={{ marginBottom: '1rem' }}>
        <label>Grado di priorità nell\'implementazione o potenziamento delle pratiche aziendali:</label>
        <input type="radio" name="priorità" value={formData.priorità} onChange={handleChange} required style={{ width: '100%', padding: '8px' }}  /><label><strong>bassa</strong></label>
        <input type="radio" name="priorità" value={formData.priorità} onChange={handleChange} required style={{ width: '100%', padding: '8px' }}  /><label><strong>media</strong></label>
        <input type="radio" name="priorità" value={formData.priorità} onChange={handleChange} required style={{ width: '100%', padding: '8px' }}  /><label><strong>alta</strong></label>
        </div>

        <div style={{ marginBottom: '1rem' }}>
          <label>Note (facoltativo):</label>
          <input type="text" name="note" value={formData.note} onChange={handleChange} required style={{ width: '100%', padding: '8px' }}/>
        </div>

        <button type="submit" style={{ padding: '10px 20px', cursor: 'pointer' }}>
          Salva
        </button>
      </form>
    </div>
  );
}
