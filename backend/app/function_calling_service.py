import json
import requests
from app.config.groq_client import groq_client

# ─────────────────────────────────────────────────────────────────────────────
# FUNCTION CALLING — ChefGPT
#
# FC 1: clasificar_solicitud
#   Determina si el prompt del usuario es una petición de receta nueva,
#   una pregunta de seguimiento sobre la conversación anterior, o un mensaje
#   no relacionado con cocina. Reemplaza la clasificación manual por keywords.
#
# FC 2: buscar_receta_mealdb
#   Busca una receta en la base de datos pública TheMealDB y devuelve
#   el nombre del plato, ingredientes y pasos de preparación.
# ─────────────────────────────────────────────────────────────────────────────

MODEL_FC = "llama-3.1-8b-instant"

TOOL_CLASIFICAR = {
    "type": "function",
    "function": {
        "name": "clasificar_solicitud",
        "description": (
            "Clasifica el mensaje del usuario en una de tres categorías: "
            "'receta' si pide una receta o cómo preparar un plato, "
            "'seguimiento' si hace una pregunta sobre algo mencionado antes en la conversación, "
            "'otro' si no tiene relación con cocina o recetas."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "categoria": {
                    "type": "string",
                    "enum": ["receta", "seguimiento", "otro"],
                    "description": "Categoría del mensaje del usuario."
                },
                "plato": {
                    "type": "string",
                    "description": "Nombre del plato o receta solicitada. Vacío si no aplica."
                }
            },
            "required": ["categoria"]
        }
    }
}

TOOL_BUSCAR_MEALDB = {
    "type": "function",
    "function": {
        "name": "buscar_receta_mealdb",
        "description": (
            "Busca una receta en la base de datos TheMealDB por nombre del plato. "
            "Devuelve ingredientes con cantidades y pasos de preparación."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "plato": {
                    "type": "string",
                    "description": "Nombre del plato a buscar en inglés o español."
                }
            },
            "required": ["plato"]
        }
    }
}


def fc_clasificar_solicitud(prompt: str) -> dict:
    """
    FC 1: Usa Function Calling para clasificar el prompt del usuario.
    Devuelve {"categoria": "receta"|"seguimiento"|"otro", "plato": str}
    """
    if not groq_client:
        return _clasificar_fallback(prompt)

    try:
        response = groq_client.chat.completions.create(
            model=MODEL_FC,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Eres un clasificador de mensajes para una app de recetas. "
                        "Debes llamar SIEMPRE a la función clasificar_solicitud con el resultado."
                    )
                },
                {"role": "user", "content": prompt}
            ],
            tools=[TOOL_CLASIFICAR],
            tool_choice={"type": "function", "function": {"name": "clasificar_solicitud"}},
            temperature=0.0,
            max_tokens=100
        )

        tool_call = response.choices[0].message.tool_calls[0]
        resultado = json.loads(tool_call.function.arguments)
        print(f"[FC1 clasificar_solicitud] resultado: {resultado}")
        return resultado

    except Exception as e:
        print(f"[FC1 clasificar_solicitud] error: {e} — usando fallback")
        return _clasificar_fallback(prompt)


def _clasificar_fallback(prompt: str) -> dict:
    prompt_lower = prompt.lower()
    indicadores_receta = ["receta", "preparar", "cómo se hace", "dame una receta", "ingredientes"]
    indicadores_seguimiento = ["anterior", "dijiste", "esa receta", "repite", "sobre eso"]

    if "receta" in prompt_lower:
        return {"categoria": "receta", "plato": prompt}
    if any(w in prompt_lower for w in indicadores_seguimiento):
        return {"categoria": "seguimiento", "plato": ""}
    if any(w in prompt_lower for w in indicadores_receta):
        return {"categoria": "receta", "plato": prompt}
    return {"categoria": "otro", "plato": ""}


def fc_buscar_receta_mealdb(plato: str) -> str | None:
    """
    FC 2: Usa Function Calling para que el LLM decida qué buscar en MealDB,
    ejecuta la búsqueda real y devuelve el resultado formateado.
    """
    if not groq_client:
        return _ejecutar_busqueda_mealdb(plato)

    try:
        response = groq_client.chat.completions.create(
            model=MODEL_FC,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Eres un asistente culinario. Cuando el usuario pida una receta, "
                        "llama a buscar_receta_mealdb con el nombre del plato en inglés."
                    )
                },
                {"role": "user", "content": f"Busca la receta de: {plato}"}
            ],
            tools=[TOOL_BUSCAR_MEALDB],
            tool_choice={"type": "function", "function": {"name": "buscar_receta_mealdb"}},
            temperature=0.0,
            max_tokens=100
        )

        tool_call = response.choices[0].message.tool_calls[0]
        args = json.loads(tool_call.function.arguments)
        plato_en = args.get("plato", plato)
        print(f"[FC2 buscar_receta_mealdb] buscando: '{plato_en}'")

        resultado = _ejecutar_busqueda_mealdb(plato_en)

        if resultado is None:
            groq_client.chat.completions.create(
                model=MODEL_FC,
                messages=[
                    {"role": "assistant", "content": None, "tool_calls": [tool_call]},
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": f"No se encontraron resultados para '{plato_en}' en TheMealDB."
                    }
                ],
                max_tokens=50
            )
            return None

        groq_client.chat.completions.create(
            model=MODEL_FC,
            messages=[
                {"role": "assistant", "content": None, "tool_calls": [tool_call]},
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": resultado
                }
            ],
            max_tokens=50
        )

        return resultado

    except Exception as e:
        print(f"[FC2 buscar_receta_mealdb] error: {e} — búsqueda directa")
        return _ejecutar_busqueda_mealdb(plato)


def _ejecutar_busqueda_mealdb(plato: str) -> str | None:
    try:
        url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={plato}"
        response = requests.get(url, timeout=5)
        data = response.json()

        if not data.get("meals"):
            return None

        meal = data["meals"][0]
        ingredientes = []
        for i in range(1, 21):
            ingrediente = meal.get(f"strIngredient{i}", "").strip()
            medida = meal.get(f"strMeasure{i}", "").strip()
            if ingrediente:
                ingredientes.append(f"- {medida} {ingrediente}".strip())

        return (
            f"{meal['strMeal']}\n"
            f"Categoría: {meal['strCategory']} | Origen: {meal['strArea']}\n\n"
            f"Ingredientes:\n" + "\n".join(ingredientes) +
            f"\n\nInstrucciones:\n{meal['strInstructions'][:800]}..."
        )
    except Exception as e:
        print(f"[MealDB directo] error: {e}")
        return None
