from app.crewai_module.crew_sugerencia_nevera.crew_sugerencia_nevera import SugerenciaNeveraCrew
from app.models.Receta import Receta


def obtener_receta_por_ingredientes(ingredientes_disponibles: str) -> Receta | None:
    inputs = {
        'ingredientes_disponibles': ingredientes_disponibles
    }

    try:
        resultado = SugerenciaNeveraCrew().crew().kickoff(inputs=inputs)
        receta: Receta | None = resultado.pydantic
        if receta is None:
            print("SugerenciaNeveraCrew no devolvió Receta pydantic válida.")
        return receta
    except Exception as e:
        print(f"Error en SugerenciaNeveraCrew: {e}")
        return None
