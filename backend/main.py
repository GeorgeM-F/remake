from typing import List
from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select, SQLModel, and_, not_, or_
from database import engine, get_session
from models import AziendeBase, Aziende, AziendeCreate, AziendeRead

# Obbligatorio
app = FastAPI()

# Permette le chiamate dal frontend React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173",
                   "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === FUNZIONI DA ESEGUIRE === #

# ISCRIZIONE
@app.post("/signup", status_code=status.HTTP_201_CREATED)   # "/signup" determina l'indirizzo URL in cui viene eseguita la funzione
def signup(data: AziendeCreate, session: Session = Depends(get_session)):   # "AziendeCreate" si riferisce alla tabella che verrà modificata
    # VERIFICA SE L'UTENTE ESISTE GIA'
    statement = select(Aziende).where(or_(Aziende.ragione_sociale == data.ragione_sociale, Aziende.password == data.password))
    preesistente = session.exec(statement).first()   # primo elemento della query
    if preesistente:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ragione sociale e/o password sono già presenti nel database.",)
    # DEFINIZIONE DATI DA INSERIRE
    hashed_password = f"hashed_{data.password}"   # versione hash di "data.password"
    db_user = Aziende(
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
    # INSERIMENTO DATI
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    # EVENTUALI VALORI DA RESTITUIRE
    return {
        "message": "Registrazione effettuata con successo!",
        "username": db_user.ragione_sociale,
    }

# LOGIN
@app.post("/login", status_code=status.HTTP_200_OK)   # "/signup" determina l'indirizzo URL in cui viene eseguita la funzione
def signup(data: AziendeCreate, session: Session = Depends(get_session)):   # "AziendeCreate" si riferisce alla tabella che verrà cercata
    # VERIFICA SE L'UTENTE ESISTE
    hashed_password = f"hashed_{data.password}"
    statement = select(Aziende).where(and_(Aziende.ragione_sociale == data.ragione_sociale, Aziende.password == hashed_password))
    utente = session.exec(statement).first()   # primo elemento della query
    if not utente:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Nome utente o password errati.",)
    # EVENTUALI VALORI DA RESTITUIRE
    return {
        "message": "Login effettuato con successo!",
        "username": data.ragione_sociale,
    }

# LOGOUT

# ELENCA PROVE EFFETTUATE

# VISUALIZZA PROGRESSI

# SALVATAGGIO RISPOSTA/E

# VISUALIZZA RISULTATI

# SCARICA REPORT
