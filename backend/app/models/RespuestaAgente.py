from pydantic import BaseModel
from typing import Optional
from app.models.Receta import Receta

class RespuestaAgente(BaseModel):
    es_receta: bool
    motivo: str # Explicación de por qué es o no una receta
    receta: Optional[Receta] = None # Solo se rellena si es_receta es True