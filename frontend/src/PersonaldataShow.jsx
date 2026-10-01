import React, { useState, useEffect } from 'react';

export default function PersonaldataShow() {
  const [jsonData, setJsonData] = useState('');

  useEffect(() => {
    fetch('http://127.0.0.1:8000/personaldata')
    .then((response) => response.json())
    .then((data) => {
      setJsonData(JSON.stringify(data, null, 2));   // Converte l'oggetto JSON in una stringa formattata
    })
    .catch((error) => {
      console.error('Errore nel recupero dei dati:', error);
      setJsonData(JSON.stringify({ error: 'Impossibile caricare i dati' }));
    });
  }, []);

  return (
    <p style={{ whiteSpace: 'pre-wrap', fontFamily: 'monospace' }}>
    {jsonData || 'Caricamento in corso...'}
    </p>
  );
}
