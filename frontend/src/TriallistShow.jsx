import React, { useState, useEffect } from 'react';
import TriallistShow from './TriallistShow';
import Newtrial from './Newtrial';
import SaverForm from './SaverForm';

export default function PersonaldataShow() {
  const [jsonData, setJsonData] = useState('');
  useEffect(() => {
    fetch('http://localhost:8000/personaldata', {credentials: 'include'})   // credentials include è necessario per dati di sessione
    .then((response) => response.json())
    .then((data) => {
      setJsonData(JSON.stringify(data, null, 2));   // Converte l'oggetto JSON in una stringa formattata
    })
    .catch((error) => {
      console.error('Errore nel recupero dei dati:', error);
      setJsonData(JSON.stringify({ error: 'Impossibile caricare i dati' }));
    });
  }, []);

  const [paginattuale, cambiapagina] = useState(null);
  if (paginattuale === "TriallistShow") {
    return <TriallistShow onBack={() => cambiapagina(null)} />;
  }
  if (paginattuale === "Newtrial") {
    return <Newtrial onBack={() => cambiapagina(null)} />;
  }
  if (paginattuale === "SaverForm") {
    return <SaverForm onBack={() => cambiapagina(null)} />;
  }

  return (
    <div>
      <h1>Area Riservata</h1>
      <p style={{ whiteSpace: 'pre-wrap', fontFamily: 'monospace' }}>
      {jsonData || 'Caricamento in corso...'}
      </p>
      <hr></hr>
      <button onClick={() => cambiapagina("TriallistShow")}>Domanda</button>
      <hr></hr>
      <button onClick={() => cambiapagina("Newtrial")}>Domanda</button>
      <hr></hr>
      <button onClick={() => cambiapagina("SaverForm")}>Domanda</button>
    </div>

  );
}
