from sqlmodel import SQLModel, Field
from typing import Optional

# DEFINIZIONE TABELLE:
class AziendeBase(SQLModel):   # Definire qui tutti i campi pubblici e liberamente modificabili dall'utente:
    __tablename__ = "aziende"   # A quale tabella del database si sta facendo riferimento
    ragione_sociale: Optional[str] = Field(default=None)
    partita_iva: Optional[str] = Field(default=None)
    codice_fiscale: Optional[str] = Field(default=None)
    settore: Optional[str] = Field(default=None)
    data_creazione: Optional[str] = Field(default=None)
    sede: Optional[str] = Field(default=None)
    codice_ateco: Optional[str] = Field(default=None)
    tipo: Optional[str] = Field(default=None)
    indirizzo_email: Optional[str] = Field(default=None)
class Aziende(AziendeBase, table=True):   # Definire qui tutti i campi sensibili (es.: password) o automatizzati (es.: primary_key e foreign_key):
    id_azienda: Optional[int] = Field(default=None, primary_key=True)
    password: Optional[str] = Field(default=None)
class AziendeCreate(AziendeBase):   # Definire qui tutti i dati necessari per creare una nuova entry (esclusa la primary_key):
    password: Optional[str] = Field(default=None)
class AziendeLogin(AziendeBase):   # Definire qui solo i dati necessari per l'autenticazione (e nient'altro):
    password: str
class AziendeRead(AziendeBase):   # Definire qui tutti i dati da restituire al client (inclusa la primary_key):
    id_azienda: int

class DomandeBase(SQLModel):
    __tablename__ = "domande"
class Domande(DomandeBase, table=True):
    domanda: Optional[str] = Field(default=None)
    pilastro_es: Optional[str] = Field(default=None)
    macro_tematica: Optional[str] = Field(default=None)
    criterio_strategie: Optional[int] = Field(default=None)
    criterio_politiche: Optional[int] = Field(default=None)
    criterio_risorse: Optional[int] = Field(default=None)
    criterio_obiettivi: Optional[int] = Field(default=None)
    criterio_metriche: Optional[int] = Field(default=None)
    info: Optional[str] = Field(default=None)
    id_domanda: Optional[int] = Field(default=None, primary_key=True)
class DomandeRead(DomandeBase):
    id_domanda: int

class ProvePreassessmentBase(SQLModel):
    __tablename__ = "prove_preassessment"
class ProvePreassessment(ProvePreassessmentBase, table=True):
    id_prova: Optional[int] = Field(default=None, primary_key=True)
    id_azienda: Optional[int] = Field(default=None, foreign_key="aziende.id_azienda")
    data_prova: Optional[str] = Field(default=None)
class ProvePreassessmentCreate(ProvePreassessmentBase):
    id_azienda: int
    data_prova: str
class ProvePreassessmentRead(ProvePreassessmentBase):
    id_prova: Optional[int] = Field(default=None, primary_key=True)
    id_azienda: Optional[int] = Field(default=None, foreign_key="aziende.id_azienda")
    data_prova: Optional[str] = Field(default=None)

class QuestionariBase(SQLModel):
    __tablename__ = "questionari"
class Questionari(QuestionariBase, table=True):
    id_questionario: Optional[int] = Field(default=None, primary_key=True)
    titolo: Optional[str] = Field(default=None)

class RispostePreassessmentBase(SQLModel):
    __tablename__ = "risposte_preassessment"
    risposta: Optional[str] = Field(default=None)
    descrizione: Optional[str] = Field(default=None)
    autovalutazione: Optional[int] = Field(default=None)
    priorità: Optional[int] = Field(default=None)
    note: Optional[str] = Field(default=None)
class RispostePreassessment(RispostePreassessmentBase, table=True):
    id_risposta: Optional[int] = Field(default=None, primary_key=True)
    id_azienda: Optional[int] = Field(default=None, foreign_key="aziende.id_azienda")
    id_prova: Optional[int] = Field(default=None, foreign_key="prove_preassessment.id_prova")
    id_domanda: Optional[int] = Field(default=None, foreign_key="domande.id_domanda")
class RispostePreassessmentCreate(RispostePreassessmentBase):
    id_azienda: int
    id_prova: int
    id_domanda: int
class RispostePreassessmentRead(RispostePreassessmentBase):
    id_risposta: int

class SuggerimentiBase(SQLModel):
    __tablename__ = "suggerimenti"
class Suggerimenti(SuggerimentiBase, table=True):
    id_suggerimento: Optional[int] = Field(default=None, primary_key=True)
    tema: Optional[str] = Field(default=None)
    punteggio: Optional[str] = Field(default=None)
    testo: Optional[str] = Field(default=None)
class SuggerimentiRead(SuggerimentiBase):
    id_suggerimento: int
    tema: str
    punteggio: str
    testo: str



# ????
AziendeBase.model_rebuild()
Aziende.model_rebuild()
AziendeCreate.model_rebuild()
AziendeRead.model_rebuild()
