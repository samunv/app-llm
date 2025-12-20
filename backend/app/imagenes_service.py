import os
import requests
import json
from app.models.SolicitudReceta import SolicitudReceta
from app.models.Especificaciones import Especificaciones
from app.models.Receta import Receta
from app.utils import obtener_instrucciones_receta_desde_imagen, extraer_formato_respuesta
from app.config.gemini_client_api import respuesta_api_gemini


def generar_respuesta_ia_imagen(imagen_base64: str, tipoImagen:str, especificaciones: Especificaciones)->None|str|Receta:

    modelo_id = "gemini-2.5-flash-lite"

    instrucciones =  obtener_instrucciones_receta_desde_imagen(especificaciones=especificaciones)

    contents = _obtener_contents(imagen=imagen_base64, tipoImagen=tipoImagen)

    if contents == None:
        return None

    payload = _obtener_playload(contents=contents, instruccionesSistema=instrucciones)

    # Llamada a la API de Gemini
    respuesta = respuesta_api_gemini(payload=payload, modelo_id=modelo_id)

    # Intentamos extraer JSON de receta
    return extraer_formato_respuesta(respuesta=respuesta)


# # ---------------- FUNCIONES AUXILIARES ----------------

def _obtener_playload(contents, instruccionesSistema):
    playload = {
        "systemInstruction": {"parts": [{"text": instruccionesSistema}]},
         "contents": contents
     }
    return playload

def _obtener_contents(imagen:str, tipoImagen:str)->list|None:
    contents = []

    if imagen and tipoImagen:

         contents.append({
             "role": "user",
             "parts": [
                 {"text": "Genera una receta a partir de esta imagen"},
               {
                    "inline_data": {
                    "data": imagen,
                    "mime_type": tipoImagen
                   }
                 }
             ]
         })
    else:
        return None

    return contents

