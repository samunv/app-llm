import json
from app.crewai_module.crew_sugerencia_nevera.crew_sugerencia_nevera import SugerenciaNeveraCrew
from app.models.Receta import Receta


def obtener_receta_por_ingredientes(ingredientes_disponibles: str) -> Receta | None:
    inputs = {
        'ingredientes_disponibles': ingredientes_disponibles
    }

    try:
        resultado = SugerenciaNeveraCrew().crew().kickoff(inputs=inputs)

        if resultado.pydantic:
            return resultado.pydantic

        raw = resultado.raw.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        raw = raw.strip()
        data = json.loads(raw)
        return Receta(**data)

    except Exception as e:
        print(f"Error en SugerenciaNeveraCrew: {e}")
        return None
