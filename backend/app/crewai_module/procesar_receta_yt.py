import re
import json
from app.models.RespuestaAgente import RespuestaAgente
from app.crewai_module.crew_receta_yt.crew_receta_yt import RecetaCrew # Importa tu clase decorada
from app.models.Receta import Receta

def procesar_receta_yt(titulo: str, video_id: str) -> Receta | None:
    inputs = {
        'titulo': titulo,
        'video_id': video_id  # Usamos el video_id para buscar en ChromaDB
    }

    resultado_crew = RecetaCrew().crew().kickoff(inputs=inputs)

    datos: RespuestaAgente | None = resultado_crew.pydantic

    if datos is None:
        try:
            # Limpiar bloque <tool_call>...<tool_call> antes de parsear
            raw_limpio = re.sub(r'<tool_call>.*?<tool_call>', '', resultado_crew.raw, flags=re.DOTALL).strip()
            raw_dict = json.loads(raw_limpio)
            datos = RespuestaAgente(**raw_dict)
        except Exception as e:
            print(f"Error parseando manualmente: {e}")
            return None

    return datos.receta if datos.es_receta else None