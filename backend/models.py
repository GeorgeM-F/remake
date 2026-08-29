from sqlmodel import SQLModel, Field
from typing import Optional

# PRE-DEFINIZIONE TABELLE (ESCLUSI I CAMPI DI TIPO "PRIMARY_KEY"):
class AziendeBase(SQLModel):
    ragione_sociale: Optional[str] = Field(default=None)
    partita_iva: Optional[str] = Field(default=None)
    codice_fiscale: Optional[str] = Field(default=None)
    settore: Optional[str] = Field(default=None)
    data_creazione: Optional[str] = Field(default=None)
    sede: Optional[str] = Field(default=None)
    codice_ateco: Optional[str] = Field(default=None)
    tipo: Optional[str] = Field(default=None)
    indirizzo_email: Optional[str] = Field(default=None)
    password: Optional[str] = Field(default=None)

class DomandeBase(SQLModel):
    domanda: Optional[str] = Field(default=None)
    pilastro_es: Optional[str] = Field(default=None)
    macro_tematica: Optional[str] = Field(default=None)
    criterio_strategie: Optional[int] = Field(default=None)
    criterio_politiche: Optional[int] = Field(default=None)
    criterio_risorse: Optional[int] = Field(default=None)
    criterio_obiettivi: Optional[int] = Field(default=None)
    criterio_metriche: Optional[int] = Field(default=None)
    info: Optional[str] = Field(default=None)

class ProvePreassessmentBase(SQLModel):
    id_azienda: Optional[int] = Field(default=None, foreign_key="aziende.id_azienda")
    data_prova: Optional[str] = Field(default=None)

class QuestionariBase(SQLModel):
    titolo: Optional[str] = Field(default=None)

class RispostePreassessmentBase(SQLModel):
    id_azienda: Optional[int] = Field(default=None, foreign_key="aziende.id_azienda")
    id_prova: Optional[int] = Field(default=None, foreign_key="prove_preassessment.id_prova")
    id_domanda: Optional[int] = Field(default=None, foreign_key="domande.id_domanda")
    risposta: Optional[str] = Field(default=None)
    descrizione: Optional[str] = Field(default=None)
    autovalutazione: Optional[int] = Field(default=None)
    priorità: Optional[int] = Field(default=None)
    note: Optional[str] = Field(default=None)

class SuggerimentiBase(SQLModel):
    tema: Optional[str] = Field(default=None)
    punteggio: Optional[str] = Field(default=None)
    testo: Optional[str] = Field(default=None)

# DEFINIZIONE TABELLE (INCLUDE I CAMPI DI TIPO "PRIMARY_KEY"):
class Aziende(AziendeBase, table=True):
    id_azienda: Optional[int] = Field(default=None, primary_key=True)

class Domande(DomandeBase, table=True):
    id_domanda: Optional[int] = Field(default=None, primary_key=True)

class ProvePreassessment(ProvePreassessmentBase, table=True):
    id_prova: Optional[int] = Field(default=None, primary_key=True)

class Questionari(QuestionariBase, table=True):
    id_questionario: Optional[int] = Field(default=None, primary_key=True)

class RispostePreassessment(RispostePreassessmentBase, table=True):
    id_risposta: Optional[int] = Field(default=None, primary_key=True)

class Suggerimenti(SuggerimentiBase, table=True):
    id_suggerimento: Optional[int] = Field(default=None, primary_key=True)





# DA QUI IN POI E' POSSIBILE SPOSTARE IL TUTTO SU "SCHEMAS.PY"
# 3. Schema per la creazione (POST, payload in ingresso, senza ID)
class AziendeCreate(AziendeBase):
    pass

class DomandeCreate(DomandeBase):
    pass

class ProvePreassessmentCreate(ProvePreassessmentBase):
    pass

class QuestionariCreate(QuestionariBase):
    pass

class RispostePreassessmentCreate(RispostePreassessmentBase):
    pass

class SuggerimentiCreate(SuggerimentiBase):
    pass

# 4. Schema per la lettura (GET, payload in uscita, garantisce la presenza dell'ID)
class AziendeRead(AziendeBase):
    id_azienda: int

class DomandeRead(DomandeBase):
    id_domanda: int

class ProvePreassessmentRead(ProvePreassessmentBase):
    id_prova: int

class QuestionariRead(QuestionariBase):
    id_questionario: int

class RispostePreassessmentRead(RispostePreassessmentBase):
    id_risposta: int

class SuggerimentiRead(SuggerimentiBase):
    id_suggerimento: int



# Fare il rebuild per ogni classe
AziendeBase.model_rebuild()
Aziende.model_rebuild()
AziendeCreate.model_rebuild()
AziendeRead.model_rebuild()
