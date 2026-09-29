from typing import List
from fastapi import FastAPI, Depends, Request, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from sqlmodel import Session, select, SQLModel, func, and_, not_, or_
from database import engine, get_session
from datetime import datetime, timezone
from models import Aziende, AziendeCreate, AziendeLogin, AziendeRead, Domande, DomandeRead, ProvePreassessment, ProvePreassessmentCreate, ProvePreassessmentRead, RispostePreassessment, RispostePreassessmentCreate, RispostePreassessmentRead
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
        "message": "Registrazione effettuata con successo!"
    }

# === FUNZIONE DI ACCESSO (GET) === #
@app.get("/login", status_code=status.HTTP_200_OK)
def login(request: Request, data: AziendeLogin, session: Session = Depends(get_session)):
    # VERIFICA SE L'UTENTE ESISTE
    hashed_password = f"hashed_{data.password}"
    statement = select(Aziende).where(and_(Aziende.ragione_sociale == data.ragione_sociale, Aziende.password == hashed_password))
    utente = session.exec(statement).first()   # primo elemento della query
    if not utente:   # se non esiste...
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Nome azienda o password errati.",)
    # SALVATAGGIO ID UTENTE NELLA SESSIONE
    request.session["azienda_attuale"] = utente.id_azienda
    # EVENTUALI VALORI DA RESTITUIRE NELLA RISPOSTA
    return {
        "message": "Login effettuato con successo!"
    }

# === FUNZIONE DI ELENCO DATI UTENTE (GET) === #
@app.get("/personaldata", status_code=status.HTTP_200_OK)
def personaldata(request: Request, data: AziendeRead, session: Session = Depends(get_session)):
    statement = select(Aziende).where(Aziende.id_azienda == int(request.session.get("azienda_attuale")))
    lista = session.exec(statement).all()   # elementi della query
    return {
        "message": "Query effettuata con successo",
        "dati azienda": lista
    }

# === FUNZIONE DI USCITA === #

# === FUNZIONE DI AGGIUNTA NUOVA PROVA (POST) === #
@app.post("/newtrial", status_code=status.HTTP_201_CREATED)
def newtrial(request: Request, data: ProvePreassessmentCreate, session: Session = Depends(get_session)):
    # ERRORE DI CONTROLLO PER IL COLLAUDO
    utente = request.session.get("azienda_attuale")
    if not utente:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nessuna azienda autenticata",)
    # DEFINIZIONE DATI DA INSERIRE
    new_data = ProvePreassessment(   # elenco dati da inserire
        id_azienda=request.session.get("azienda_attuale"),
        data_prova=datetime.now(timezone.utc)
    )
    # INSERIMENTO DATI...
    session.add(new_data)   # ...nella sessione
    session.commit()   # ...dalla sessione al database (solo le ultime modifiche, e senza usare una query SQL)
    session.refresh(new_data)
    return {
        "message": "Nuova prova registrata!"
    }

# === FUNZIONE DI ELENCO PROVE EFFETTUATE (GET) === #
@app.get("/triallist", status_code=status.HTTP_200_OK)
def triallist(request: Request, data: ProvePreassessmentRead, session: Session = Depends(get_session)):
    statement = select(ProvePreassessment).where(ProvePreassessment.id_azienda == int(request.session.get("azienda_attuale")))
    lista = session.exec(statement).all()   # elementi della query
    return {
        "message": "Query effettuata con successo",
        "lista prove": lista
    }

# === FUNZIONE DI CARICAMENTO PROVA (GET) === #   # rivedere il modo in cui viene scelto l'id della prova
@app.get("/loadt/{i}", status_code=status.HTTP_200_OK)   # "i" dipende dalla pagina attuale;
def loadt(i: int, request: Request, session: Session = Depends(get_session)):   # "i" viene ridichiarato tra gli argomenti della funzione
    request.session["prova_attuale"] = i
    return {
        "message": "Caricamento effettuato con successo",
        "id prova": i
    }

# === FUNZIONE DI CARICAMENTO PROSSIMA DOMANDA (GET) === #
@app.get("/loadq/{i}", status_code=status.HTTP_200_OK)   # "i" dipende dalla pagina attuale;
def loadq(i: int, request: Request, data: DomandeRead, session: Session = Depends(get_session)):   # "i" viene ridichiarato tra gli argomenti della funzione
    statement = select(Domande).where(Domande.id_domanda == i)
    dom = session.exec(statement).first()
    request.session["domanda_attuale"] = dom.id_domanda
    return {
        "message": "Query effettuata con successo",
        "domanda": dom
    }

# === FUNZIONE DI SALVATAGGIO RISPOSTE (POST) === #   (INSERIRE ANCHE LA SOVRASCRITTURA)
@app.post("/saver/{i}", status_code=status.HTTP_201_CREATED)
def saver(i: int, request: Request, data: RispostePreassessmentCreate, session: Session = Depends(get_session)):
    new_data = RispostePreassessment(
        id_azienda=request.session.get("azienda_attuale"),
        id_prova=request.session.get("prova_attuale"),
        id_domanda=i,
        risposta=data.risposta,
        descrizione=data.descrizione,
        autovalutazione=data.autovalutazione,
        priorità=data.priorità,
        note=data.note
    )
    session.add(new_data)
    session.commit()
    session.refresh(new_data)
    return {
        "message": "Risposte registrate con successo!"
    }

# === FUNZIONE DI VISUALIZZAZIONE RISPOSTE (GET) === #
@app.get("/loadr/{i}", status_code=status.HTTP_200_OK)
def loadr(i: int, request: Request, data: RispostePreassessmentRead, session: Session = Depends(get_session)):
    statement = select(RispostePreassessment).where(RispostePreassessment.id_domanda == i)
    risposte = session.exec(statement).all()   # elementi della query
    return {
        "message": "Query effettuata con successo",
        "risposte": risposte
    }

# === FUNZIONE DI CALCOLO E VISUALIZZAZIONE RISULTATI (GET) === #
@app.get("/result", status_code=status.HTTP_200_OK)
def result(request: Request, data: RispostePreassessmentRead, session: Session = Depends(get_session)):
    # NUMERO DI RISPOSTE "NO"
    statementa = select(func.count()).select_from(RispostePreassessment).where(and_(RispostePreassessment.id_azienda == int(request.session.get("azienda_attuale")), RispostePreassessment.id_prova == int(request.session.get("prova_attuale")), RispostePreassessment.risposta == "no"))
    numsi = session.exec(statementa).one()
    # NUMERO DI RISPOSTE "IN PARTE"
    statementb = select(func.count()).select_from(RispostePreassessment).where(and_(RispostePreassessment.id_azienda == int(request.session.get("azienda_attuale")), RispostePreassessment.id_prova == int(request.session.get("prova_attuale")), RispostePreassessment.risposta == "in parte"))
    numni = session.exec(statementb).one()
    # NUMERO DI RISPOSTE "SI'"
    statementc = select(func.count()).select_from(RispostePreassessment).where(and_(RispostePreassessment.id_azienda == int(request.session.get("azienda_attuale")), RispostePreassessment.id_prova == int(request.session.get("prova_attuale")), RispostePreassessment.risposta == "sì"))
    numno = session.exec(statementc).one()
    # DEFINIZIONE TABELLA VALS DA USARE PER I CALCOLI
    statementd = select(RispostePreassessment).where(and_(RispostePreassessment.id_azienda == int(request.session.get("azienda_attuale")), RispostePreassessment.id_prova == int(request.session.get("prova_attuale"))))
    resultsd = session.exec(statementd).all()

    # DEFINIZIONE VALORI FINALI
    # e1 = sommatoria(vals[0])/5
    # e2 = sommatoria(vals[1])/5
    # e3 = sommatoria(vals[2])/5
    # e4 = sommatoria(vals[3])/5
    # e5 = sommatoria(vals[4])/5
    # s1 = sommatoria(vals[5])/5
    # s2 = sommatoria(vals[6])/5
    # s3 = sommatoria(vals[7])/5
    # s4 = sommatoria(vals[8])/5
    # g1 = sommatoria(vals[9])/5
    # strategie = (vals[0][0]+vals[1][0]+vals[2][0]+vals[3][0]+vals[4][0]+vals[5][0]+vals[6][0]+vals[7][0]+vals[8][0]+vals[9][0])/10
    # politiche = (vals[0][1]+vals[1][1]+vals[2][1]+vals[3][1]+vals[4][1]+vals[5][1]+vals[6][1]+vals[7][1]+vals[8][1]+vals[9][1])/10
    # risorse = (vals[0][2]+vals[1][2]+vals[2][2]+vals[3][2]+vals[4][2]+vals[5][2]+vals[6][2]+vals[7][2]+vals[8][2]+vals[9][2])/10
    # obiettivi = (vals[0][3]+vals[1][3]+vals[2][3]+vals[3][3]+vals[4][3]+vals[5][3]+vals[6][3]+vals[7][3]+vals[8][3]+vals[9][3])/10
    # metriche = (vals[0][4]+vals[1][4]+vals[2][4]+vals[3][4]+vals[4][4]+vals[5][4]+vals[6][4]+vals[7][4]+vals[8][4]+vals[9][4])/10
    # environmental = (e1+e2+e3+e4+e5)/5
    # social = (s1+s2+s3+s4)/4
    # governance = (g1)/1
    # complessivo = (environmental+social+governance)/3

    return {
        "message": "Query effettuata con successo",
        "numero sì": numsi,
        "numero in parte": numni,
        "numero no": numno
    }

# === FUNZIONE DI SCARICAMENTO REPORT (GET) === #
