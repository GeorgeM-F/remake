import React, { useState } from 'react';
// IMPORTA TUTTE LE FUNZIONI DEFINITE NEI FILE PRESENTI IN QUESTA CARTELLA //
import SignupForm from './SignupForm';
import LoginForm from './LoginForm';
import PersonaldataShow from './PersonaldataShow';

function App() {
  const [paginattuale, cambiapagina] = useState(null);
  if (paginattuale === "SignupForm") {
    return <SignupForm onBack={() => cambiapagina(null)} />;   // inserisce la funzione "onBack" all'interno di SignupForm in modo che sia possibile usarla nel relativo codice (dopo averla scritta tra parentesi graffe durante la definizione)
  }
  if (paginattuale === "LoginForm") {
    return <LoginForm onBack={() => cambiapagina(null)} />;
  }
  if (paginattuale === "PersonaldataShow") {
    return <PersonaldataShow onBack={() => cambiapagina(null)} />;
  }
  return (
    <div>
      <h1>Pre-assessment</h1>
      <hr></hr>
      <button onClick={() => cambiapagina("SignupForm")}>Iscriviti</button>
      <hr></hr>
      <button onClick={() => cambiapagina("LoginForm")}>Accedi</button>
      <hr></hr>
      <button onClick={() => cambiapagina("PersonaldataShow")}>Area Riservata</button>
    </div>
  );
}

export default App;
