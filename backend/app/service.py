import os
import requests
import json
from dotenv import load_dotenv
from app.models.SolicitudReceta import SolicitudReceta
from app.models.Especificaciones import Especificaciones
from app.models.Receta import Receta

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")


def generar_respuesta_ia(datos_solicitud: SolicitudReceta):
    if not api_key:
        return {"error": "Falta la API Key en el archivo .env"}

    modelo_id = datos_solicitud.modeloIASeleccionado or "gemini-2.5-flash"

    # Preparamos el contenido del chat con historial + nuevo mensaje
    contents = datos_solicitud.historial.copy() 
    if datos_solicitud.imagen and datos_solicitud.tipoImagen:
    # Mensaje con imagen y texto
        contents.append({
        "role": "user",
        "parts": [
            {"text": datos_solicitud.comida},
            {"inline_data": {"data": datos_solicitud.imagen, "mime_type": datos_solicitud.tipoImagen}}
        ]
        })
    else:
    # Solo texto
        contents.append({
        "role": "user",
        "parts": [{"text": datos_solicitud.comida}]
        })

    # Instrucciones generales: crear receta o responder sobre existente
    instrucciones = _obtener_instrucciones(datos_solicitud)

    payload = {
        "systemInstruction": {"parts": [{"text": instrucciones}]},
        "contents": contents
    }

    # Llamada a la API de Gemini
    respuesta = _llamar_api_gemini(payload, modelo_id)

    # Intentamos extraer JSON de receta
    try:
        json_str = extraerJSON(respuesta)
        json_receta = json.loads(json_str)
        if "nombrePlato" in json_receta:
            return Receta(
                json_receta.get("nombrePlato"),
                json_receta.get("ingredientes"),
                json_receta.get("pasos"),
                json_receta.get("especificaciones", "")
            )
    except Exception:
        # Si no es JSON, devolvemos texto plano (chat)
        return respuesta


# ---------------- FUNCIONES AUXILIARES ----------------

def _llamar_api_gemini(payload, modelo_id):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo_id}:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        resultado = response.json()
        return resultado["candidates"][0]["content"]["parts"][0]["text"].strip()
    except Exception as e:
        raise Exception(f"Error al llamar Gemini: {e}")


def _obtener_instrucciones(datos_solicitud: SolicitudReceta):
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
    "ingredientes": ["Ingrediente 1", "Ingrediente 2"],
    "pasos": ["Paso 1", "Paso 2"],
    "especificaciones": "Especificaciones del usuario si las hay"
}}

Si el prompt no es sobre comida, puedes responder en texto plano sobre la receta anterior. Y si no
hay receta anterior, deberás indicarle al usuario que debe pedir una receta sobre comida o platos de comidas.

## PETICIÓN DEL USUARIO
Prompt: "{comida}"

## ESPECIFICACIONES
Tipo de dieta: "{especificaciones.tipo_dieta}"
Restricciones: "{especificaciones.restricciones}"
Objetivo: "{especificaciones.objetivo}"
"""


def extraerJSON(texto):
    inicio = texto.find("{")
    fin = texto.rfind("}") + 1
    if inicio == -1 or fin == -1:
        raise Exception("No se encontró JSON en la respuesta")
    return texto[inicio:fin]
