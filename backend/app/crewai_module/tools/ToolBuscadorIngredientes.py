from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from app.rag_service.rag_transcripciones_service import obtener_fragmentos_mediante_prompt_usuario


class ToolBuscadorIngredientesInput(BaseModel):
    ingredientes: str = Field(
        description="Lista de ingredientes disponibles separados por comas."
    )


class ToolBuscadorIngredientes(BaseTool):
    name: str = "Buscador_Recetas_Por_Ingredientes"
    description: str = (
        "Busca en la memoria de videos guardados si existe alguna receta "
        "que pueda prepararse con los ingredientes proporcionados. "
        "Usa esta tool al inicio para aprovechar el conocimiento almacenado antes de inventar."
    )
    args_schema: type[BaseModel] = ToolBuscadorIngredientesInput

    def _run(self, ingredientes: str) -> str:
        fragmentos = obtener_fragmentos_mediante_prompt_usuario(ingredientes)
        if not fragmentos:
            return "No se encontraron recetas guardadas con esos ingredientes. Usa tu conocimiento propio."
        return "\n---\n".join(fragmentos)
