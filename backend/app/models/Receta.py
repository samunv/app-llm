from pydantic import BaseModel
from typing import List, Optional # Usamos typing para las listas
class Ingrediente(BaseModel):
    nombre: str
    cantidad: Optional[str | int | float] = None
    unidadMedida: Optional[str] = ""

class Receta(BaseModel):
    nombrePlato: str
    ingredientes: List[Ingrediente] 
    pasos: List[str]
    especificaciones: Optional[str] = None
