import os
import requests
import json
from dotenv import load_dotenv
from app.models.SolicitudReceta import SolicitudReceta
from app.models.Especificaciones import Especificaciones
from app.models.Receta import Receta
from app.utils import obtener_instrucciones, extraer_formato_respuesta

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")


def generar_respuesta_ia(datos_solicitud: SolicitudReceta):
    if not api_key:
        return {"error": "Falta la API Key en el archivo .env"}

    modelo_id = datos_solicitud.modeloIASeleccionado or "gemini-2.5-flash"

    # Preparamos el contenido del chat con historial + nuevo mensaje
    contents = _obtener_contents_con_historial(datos_solicitud=datos_solicitud)

    # Instrucciones generales: crear receta o responder sobre existente
    instrucciones = obtener_instrucciones(datos_solicitud)

    payload = _obtener_playload(contents=contents, instruccionesSistema=instrucciones)

    # Llamada a la API de Gemini
    respuesta = _llamar_api_gemini(payload, modelo_id)

    # Intentamos extraer JSON de receta
    return extraer_formato_respuesta(respuesta=respuesta)


# ---------------- FUNCIONES AUXILIARES ----------------

def _obtener_playload(contents, instruccionesSistema):
    playload = {
        "systemInstruction": {"parts": [{"text": instruccionesSistema}]},
        "contents": contents
    }
    return playload

def _obtener_contents_con_historial(datos_solicitud):
    contents = datos_solicitud.historial.copy()

    if datos_solicitud.imagen and datos_solicitud.tipoImagen:
        
        contents.append({
            "role": "user",
            "parts": [
                {"text": datos_solicitud.comida},
                {
                    "inline_data": {
                        "data": datos_solicitud.imagen,
                        "mime_type": datos_solicitud.tipoImagen
                    }
                }
            ]
        })
    else:
        contents.append({
            "role": "user",
            "parts": [
                {"text": datos_solicitud.comida}
            ]
        })

    return contents


def _llamar_api_gemini(payload: dict[str, any], modelo_id:str)->str:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo_id}:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        resultado = response.json()
        return resultado["candidates"][0]["content"]["parts"][0]["text"].strip()
    except Exception as e:
        raise Exception(f"Error al llamar Gemini: {e}")
