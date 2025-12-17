import os
import json

from app.models.SolicitudReceta import SolicitudReceta
from app.models.Especificaciones import Especificaciones
from app.models.Receta import Receta
from app.utils import obtener_instrucciones_generador_recetas, extraer_formato_respuesta
from app.config.groq_client import respuesta_cliente_groq


def generar_respuesta_ia(datos_solicitud: SolicitudReceta = {}, fuente_info:str = ""):
    """
    Genera una respuesta de la IA (receta o chat) usando el SDK de Groq.
    """

    # Usamos el modelo seleccionado o un valor predeterminado compatible con Groq.
    modelo_id = datos_solicitud.modeloIASeleccionado or "llama-3.1-8b-instant"

    messages = _obtener_messages_con_historial(datos_solicitud=datos_solicitud)
    system_prompt = obtener_instrucciones_generador_recetas(datos_solicitud=datos_solicitud, fuente_info=fuente_info if fuente_info else "")

    # Llamada a la API usando el SDK
    try:
        respuesta = _llamar_api_sdk(messages=messages, 
                                    system_prompt=system_prompt, 
                                    modelo_id=modelo_id)
    except Exception as e:
        return {"error": str(e)}

    # Intentamos extraer JSON de receta
    return extraer_formato_respuesta(respuesta=respuesta)

def _obtener_messages_con_historial(datos_solicitud: SolicitudReceta):
    """
    Transforma el historial y la nueva solicitud al formato 'messages' 
    requerido por el SDK de Groq 
    """
    messages = []

    for mensaje_ia in datos_solicitud.historial:
        role = "assistant" if mensaje_ia["role"] == "model" else "user"
        text = mensaje_ia["parts"][0]["text"]
        messages.append({
            "role": role,
            "content": text
        })

    # Añadimos el nuevo mensaje del usuario
    user_content = []
    user_content.append(datos_solicitud.prompt)
    # Unimos el contenido en una sola cadena para el mensaje del usuario
    messages.append({
        "role": "user",
        "content": "\n".join(user_content)
    })

    return messages


def _llamar_api_sdk(messages: list[dict], system_prompt: str, modelo_id:str)->str:
   return respuesta_cliente_groq(messages=messages, system_prompt=system_prompt, modelo_id=modelo_id)