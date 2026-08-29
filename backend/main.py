from typing import List
from fastapi import FastAPI, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select, SQLModel
from sqlmodel import and_, not_, or_, select
from database import engine, get_session
from models import AziendeBase, Aziende, AziendeCreate, AziendeRead

# Inizializza FastAPI
app = FastAPI()

# Permette le chiamate dal frontend React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Funzioni da eseguire

# ISCRIZIONE
@app.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(
    data: AziendeCreate,
    session: Session = Depends(get_session)
):
    # verifica se l'utente esiste già
    statement = select(Aziende).where(or_(Aziende.ragione_sociale == data.ragione_sociale, Aziende.password == data.password))
    existing_user = session.exec(statement).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ragione sociale e/o password sono già presenti nel database.",
        )
    # hash della password
    hashed_password = f"hashed_{data.password}"
    # salvataggio nel database
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
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return {
        "message": "[AVVISO SUCCESSO]",
        "username": db_user.ragione_sociale,
    }

# LOGIN

# LOGOUT

# ELENCA PROVE EFFETTUATE

# VISUALIZZA PROGRESSI

# SALVATAGGIO RISPOSTA/E

# VISUALIZZA RISULTATI

# SCARICA REPORT
