import React from 'react';
// IMPORTA TUTTE LE FUNZIONI DEFINITE NEI FILE PRESENTI IN QUESTA CARTELLA //
import SignupForm from './SignupForm';
import LoginForm from './LoginForm';
import PersonaldataShow from './PersonaldataShow';
// import Newtrial from './Newtrial';
// import TriallistShow from './TriallistShow';
// import LoadtShow from './LoadtShow';
// import LoadqShow from '.LoadqShow';
import SaverForm from './SaverForm';
// import LoadrShow from './LoadrShow';
// import ResultShow from './ResultShow';

function App() {
  return (
    <div>
      <SignupForm />
      <LoginForm />
      <PersonaldataShow />
      <SaverForm />
    </div>
  );
}

export default App;
