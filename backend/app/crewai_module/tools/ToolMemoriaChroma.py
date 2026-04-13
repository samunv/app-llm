# Definimos la herramienta que usa TU lógica de Chroma
from crewai.tools import BaseTool
from app.rag_service.rag_transcripciones_service import obtener_fragmentos_ingredientes, obtener_fragmentos_pasos
from app.models.VideoInfo import VideoInfo

# Function Calling a ChromaDB
class ToolMemoriaChroma(BaseTool):
    name: str = "Buscador_Memoria_Chef"
    description: str = "Busca fragmentos de recetas en videos guardados anteriormente."

    def _run(self, video_id: str) -> str:
        # Intentamos obtener fragmentos relevantes (RAG)
        # Buscamos específicamente ingredientes y pasos
        fragmentos = obtener_fragmentos_ingredientes(video_id) + obtener_fragmentos_pasos(video_id)


        if not fragmentos:
            return "No hay antecedentes de esta receta en la base de datos."
        return "\n".join(fragmentos)
    







