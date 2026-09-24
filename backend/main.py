from typing import List
from fastapi import FastAPI, Depends, Request, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from sqlmodel import Session, select, SQLModel, and_, not_, or_
from database import engine, get_session
from datetime import datetime, timezone
from models import Aziende, AziendeCreate, AziendeRead, ProvePreassessment, ProvePreassessmentCreate
app = FastAPI()   # Obbligatorio
app.add_middleware(   # Permette le chiamate dal frontend React
    CORSMiddleware,
    allow_origins=["http://localhost:5173",
                   "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key="chiave-temporanea-per-sviluppo-locale", max_age=7200)   # Inizializzazione sessione (max_age=durata in secondi)



# === FUNZIONE DI ISCRIZIONE (POST) === #
@app.post("/signup", status_code=status.HTTP_201_CREATED)   # "/signup" determina l'indirizzo URL in cui viene eseguita la funzione
def signup(request: Request, data: AziendeCreate, session: Session = Depends(get_session)):   # "AziendeCreate" è la tabella da usare come modello di richiesta
    # VERIFICA SE L'UTENTE ESISTE GIA'
    statement = select(Aziende).where(or_(Aziende.ragione_sociale == data.ragione_sociale, Aziende.password == data.password))   # Definisce la query SQL
    preesistente = session.exec(statement).first()   # primo elemento della query
    if preesistente:   # se "preesistente" esiste...
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ragione sociale e/o password sono già presenti nel database.",)   # Interrompe l'esecuzione e risponde con un errore
    # DEFINIZIONE DATI DA INSERIRE
    hashed_password = f"hashed_{data.password}"   # versione hash di "data.password"
    new_data = Aziende(   # elenco dati da inserire
        ragione_sociale=data.ragione_sociale,
        partita_iva=data.partita_iva,
        codice_fiscale=data.codice_fiscale,
        settore=data.settore,
        data_creazione=data.data_creazione,
        sede=data.sede,
        codice_ateco=data.codice_ateco,
        tipo=data.tipo,
        indirizzo_email=data.indirizzo_email,
        password=hashed_password
    )
    # INSERIMENTO DATI...
    session.add(new_data)   # ...nella sessione
    session.commit()   # ...dalla sessione al database (solo le ultime modifiche, e senza usare una query SQL)
    session.refresh(new_data)
    # EVENTUALI VALORI DA RESTITUIRE NELLA RISPOSTA
    return {
        "message": "Registrazione effettuata con successo!",
        "username": new_data.ragione_sociale,
    }

# === FUNZIONE DI ACCESSO (GET) === #
@app.post("/login", status_code=status.HTTP_200_OK)
def login(request: Request, data: AziendeRead, session: Session = Depends(get_session)):
    # VERIFICA SE L'UTENTE ESISTE
    hashed_password = f"hashed_{data.password}"
    statement = select(Aziende).where(and_(Aziende.ragione_sociale == data.ragione_sociale, Aziende.password == hashed_password))
    utente = session.exec(statement).first()   # primo elemento della query
    if not utente:   # se non esiste...
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Nome utente o password errati.",)
    # SALVATAGGIO ID UTENTE NEL DATABASE
    request.session["utente_attuale"] = utente.id_azienda
    # EVENTUALI VALORI DA RESTITUIRE NELLA RISPOSTA
    return {
        "message": "Login effettuato con successo!",
        "username": utente.ragione_sociale,
        "utente_attuale": utente.id_azienda,
    }

# === FUNZIONE DI USCITA (GET) === #

# === FUNZIONE DI AGGIUNTA NUOVA PROVA (POST) === #
@app.post("/newtrial", status_code=status.HTTP_201_CREATED)
def newtrial(request: Request, data: ProvePreassessmentCreate, session: Session = Depends(get_session)):
    # ERRORE DI CONTROLLO PER IL COLLAUDO
    utente = request.session.get("utente_attuale")
    if not utente:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nessuna azienda autenticata",)
    # DEFINIZIONE DATI DA INSERIRE
    new_data = ProvePreassessment(   # elenco dati da inserire
        id_azienda=request.session.get("utente_attuale"),
        data_prova=datetime.now(timezone.utc)
    )
    # INSERIMENTO DATI...
    session.add(new_data)   # ...nella sessione
    session.commit()   # ...dalla sessione al database (solo le ultime modifiche, e senza usare una query SQL)
    session.refresh(new_data)
    # EVENTUALI VALORI DA RESTITUIRE NELLA RISPOSTA
    return {
        "message": "Nuova prova registrata!",
        "data nuova prova": new_data.data_prova,
    }

# === FUNZIONE DI ELENCO PROVE EFFETTUATE (GET) === #

# === FUNZIONE DI SALVATAGGIO RISPOSTE E PROGRESSI (POST) === #

# === FUNZIONE DI VISUALIZZAZIONE RISPOSTE E PROGRESSI (GET) === #

# === FUNZIONE DI CALCOLO E VISUALIZZAZIONE RISULTATI (GET) === #

# === FUNZIONE DI SCARICAMENTO REPORT (GET) === #
