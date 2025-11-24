from app.models.SolicitudReceta import SolicitudReceta
from app.models.Especificaciones import Especificaciones
from app.models.Receta import Receta
import json

def obtener_instrucciones(datos_solicitud: SolicitudReceta):
    comida = datos_solicitud.comida or ""
    especificaciones = datos_solicitud.especificaciones or Especificaciones()

    return f"""
Eres ChefGPT, asistente experto en cocina.
Puedes crear recetas o conversar sobre recetas existentes.
Si el prompt contiene comida, genera un JSON de receta
PERO SOLO SI NO EXISTE UNA RECETA ANTERIOR, DE LO CONTRARIO DEVOLVERÁS UN TEXTO PLANO INDICANDO QUE SOLO PUEDES HABLAR SOBRE ESA ÚLTIMA RECETA.
Si solo pregunta sobre la receta anterior, responde en texto.

Formato JSON exacto:
{{
    "nombrePlato": "Nombre del plato",
    "ingredientes": ["Ingrediente 1", "Ingrediente 2"] (Ten en cuenta si el usuario especifica sus ingredientes),
    "pasos": ["Paso 1", "Paso 2"],
    "especificaciones": "Especificaciones del usuario si las hay, en forma de texto plano"
}}

Si el prompt no es sobre comida, puedes responder en texto plano sobre la receta anterior. Y si no
hay receta anterior, deberás indicarle al usuario que debe pedir una receta sobre comida o platos de comidas.

## PETICIÓN DEL USUARIO
Prompt: "{comida}"

## ESPECIFICACIONES
Tipo de dieta: "{especificaciones.tipo_dieta}"
Restricciones: "{especificaciones.restricciones}"
Objetivo: "{especificaciones.objetivo}"
Ingredientes: "{especificaciones.ingredientes_disponibles}" (solo tenlos en cuenta si los especifica el usuario, sino utiliza los que quieras)
"""

def extraer_formato_respuesta(respuesta):
     # Intentamos extraer JSON de receta
    try:
        json_str = _extraerJSON(respuesta)
        json_receta = json.loads(json_str)
        if "nombrePlato" in json_receta:
            return Receta(
                json_receta.get("nombrePlato"),
                json_receta.get("ingredientes"),
                json_receta.get("pasos"),
                json_receta.get("especificaciones", "")
            )
    except Exception:
        # Si no es Receta, devolvemos texto plano (chat)
        return respuesta

def _extraerJSON(texto):
    inicio = texto.find("{")
    fin = texto.rfind("}") + 1
    if inicio == -1 or fin == -1:
        raise Exception("No se encontró JSON en la respuesta")
    return texto[inicio:fin]
