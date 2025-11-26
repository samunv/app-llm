from app.models.SolicitudReceta import SolicitudReceta
from app.models.Especificaciones import Especificaciones
from app.models.Receta import Receta
import json
import re

def obtener_instrucciones(datos_solicitud: SolicitudReceta):
    comida = datos_solicitud.comida or ""
    especificaciones = datos_solicitud.especificaciones or Especificaciones()

    # Usar CUATRO llaves ({{{{ y }}}} ) para escapar el bloque JSON
    return f"""
// ROL Y OBJETIVO
Eres ChefGPT, un asistente experto en cocina. Tu función principal es generar recetas y responder preguntas sobre la ÚLTIMA receta que generaste.

// FORMATO DE RESPUESTA
1. Si el usuario pide una receta, DEVUELVE SOLO el JSON solicitado. NO añadas texto antes ni después.
2. Si el usuario pregunta sobre la receta en el historial, responde en texto plano de manera concisa.
3. Si el usuario pregunta por algo que no es comida o no hay receta en el historial, pide amablemente que solicite una receta.
4. Todas tus respuestas deben ser siempre en Español. Si el usuario trata de pedir las cosas en otro idioma, tu responderás en español.


// ESTRUCTURA JSON (OBLIGATORIA)
{{{{
    "nombrePlato": "Nombre del plato",
    "ingredientes": ["Ingrediente 1", "Ingrediente 2"],
    "pasos": ["Paso 1", "Paso 2"],
    "especificaciones": "Texto con restricciones de la dieta o notas especiales."
}}}}

// CONTEXTO DE LA SOLICITUD
PROMPT ACTUAL: "{comida}"
ESPECIFICACIONES DEL USUARIO:
- Dieta: "{especificaciones.tipo_dieta}"
- Restricciones: "{especificaciones.restricciones}"
- Objetivo: "{especificaciones.objetivo}"
- Ingredientes personalizados añadidos: "{especificaciones.ingredientes_disponibles}"
"""


def extraer_formato_respuesta(respuesta:str)->Receta | str:
    try:
        json_str = _extraerJSON(respuesta)
        json_receta = json.loads(json_str)

        if isinstance(json_receta, dict) and "nombrePlato" in json_receta:
            return Receta(
                json_receta.get("nombrePlato"),
                json_receta.get("ingredientes"),
                json_receta.get("pasos"),
                json_receta.get("especificaciones", "")
            )
    except Exception as e:
        print("Error al extraer receta:", e)

    # Devuelve texto plano si no hay JSON válido
    return respuesta 

def _extraerJSON(texto):
    """
    Extrae el primer bloque JSON válido encontrado en 'texto'.
    Devuelve '{}' si no se encuentra nada válido.
    """
    # Buscar cualquier bloque entre llaves {...} incluyendo saltos de línea
    match = re.search(r"\{.*?\}", texto, re.DOTALL)
    if match:
        return match.group()
    else:
        # Devuelve JSON vacío para que json.loads nunca falle
        return "{}"
