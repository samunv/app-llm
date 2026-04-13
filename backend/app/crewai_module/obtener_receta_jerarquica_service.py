import json
import re
from app.models.Receta import Receta
from app.crewai_module.crew_jerarquico.crew_jerarquico import CrewJerarquico
from app.function_calling_service import fc_buscar_receta_mealdb


def obtener_receta_jerarquica(plato: str) -> Receta | None:
    inputs = {'plato': plato}
    print(f"--- Iniciando Crew Jerárquica para: {plato} ---")

    resultado_crew = CrewJerarquico().crew().kickoff(inputs=inputs)

    # Intento 1: Pydantic directo
    receta_datos: Receta | None = resultado_crew.pydantic
    if receta_datos is not None:
        print(f"✅ Receta obtenida con éxito: {receta_datos.nombrePlato}")
        return receta_datos

    # Intento 2: Fallback parseo manual
    try:
        raw_output = resultado_crew.raw

        if isinstance(raw_output, Receta):
            return raw_output

        if isinstance(raw_output, dict):
            return Receta(**raw_output)

        if isinstance(raw_output, str):
            print("⚠️ Pydantic no detectado, intentando parseo manual...")

            if "RECHAZADO" in raw_output.upper():
                print(f"🛡️ Pedido rechazado: {plato}")
                return None

            raw_limpio = re.sub(r'<tool_call>.*?</tool_call>', '', raw_output, flags=re.DOTALL).strip()
            match_json = re.search(r'```json\s*(\{.*?\})\s*```|(\{.*\})', raw_limpio, re.DOTALL)
            if match_json:
                json_str = match_json.group(1) or match_json.group(2)
                raw_dict = json.loads(json_str)
                return Receta(**raw_dict)

        # ── FC 2: buscar_receta_mealdb ─────────────────────────────────────────
        # Si la Crew no pudo estructurar la receta, usamos Function Calling
        # para buscar directamente en TheMealDB. El LLM decide qué buscar
        # (puede traducir el plato al inglés) y ejecutamos el ciclo tool completo.
        print(f"[FC2] Crew sin resultado — usando fc_buscar_receta_mealdb para: {plato}")
        resultado_fc = fc_buscar_receta_mealdb(plato)
        if resultado_fc:
            print("[FC2] Resultado obtenido de MealDB via Function Calling.")
            return None

        print("❌ No se pudo determinar el formato de respuesta.")
        return None

    except Exception as e:
        print(f"❌ Error crítico parseando la receta: {e}")
        return None
