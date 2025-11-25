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
Eres ChefGPT, asistente experto en cocina.
Puedes crear recetas o conversar sobre recetas existentes.
Si el prompt contiene comida, genera un JSON de receta
PERO SOLO SI NO EXISTE UNA RECETA ANTERIOR, DE LO CONTRARIO DEVOLVERÁS UN TEXTO PLANO INDICANDO QUE SOLO PUEDES HABLAR SOBRE ESA ÚLTIMA RECETA.
Si solo pregunta sobre la receta anterior, responde en texto.
AL GENERAR UNA RECETA SOLO DEBES DEVOLVER EL JSON SIN AÑADIR NINGÚN MENSAJE NI AL PRINCIPIO NI AL FINAL DE LA RESPUESTA

Formato JSON exacto:
{{{{
    "nombrePlato": "Nombre del plato",
    "ingredientes": ["Ingrediente 1", "Ingrediente 2"] (Ten en cuenta si el usuario especifica sus ingredientes),
    "pasos": ["Paso 1", "Paso 2"],
    "especificaciones": "Especificaciones del usuario si las hay, en forma de texto plano"
}}}}

Si el prompt no es sobre comida, puedes responder en texto plano sobre la receta anterior. Y si no
hay receta anterior, deberás indicarle al usuario que debe pedir una receta sobre comida o platos de comidas.

## PETICIÓN DEL USUARIO
Prompt: "{comida}"

## ESPECIFICACIONES
Tipo de dieta: "{especificaciones.tipo_dieta}"
Restricciones: "{especificaciones.restricciones}"
Objetivo: "{especificaciones.objetivo}"
Ingredientes personalizados añadidos: "{especificaciones.ingredientes_disponibles}" (solo tenlos en cuenta si los especifica el usuario, sino utiliza los que quieras)
"""


def extraer_formato_respuesta(respuesta):
    try:
        json_str = _extraerJSON(respuesta)
        json_receta = json.loads(json_str)

        if isinstance(json_receta, dict) and "nombrePlato" in json_receta:
            from app.models.Receta import Receta
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
