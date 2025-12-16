import os
import json
from dotenv import load_dotenv
from groq import Groq # Importamos la clase Groq
from app.models.SolicitudReceta import SolicitudReceta
from app.models.Especificaciones import Especificaciones
from app.models.Receta import Receta
from app.utils import obtener_instrucciones, extraer_formato_respuesta

load_dotenv()
api_key = os.getenv("GROQ_API_KEY") 

try:
    groq_client = Groq(api_key=api_key)
except Exception as e:
    print(f"Error al inicializar el cliente Groq: {e}")
    groq_client = None


def generar_respuesta_ia(datos_solicitud: SolicitudReceta):
    """
    Genera una respuesta de la IA (receta o chat) usando el SDK de Groq.
    """
    if not groq_client:
        return {"error": "Falta la API Key en el archivo .env o es inválida"}

    # Usamos el modelo seleccionado o un valor predeterminado compatible con Groq.
    modelo_id = datos_solicitud.modeloIASeleccionado or "llama-3.1-8b-instant" 

    messages = _obtener_messages_con_historial(datos_solicitud=datos_solicitud)
    system_prompt = obtener_instrucciones(datos_solicitud)

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
    
    # TODO:Por ahora, solo añadimos el texto porque los modelos de groq no aceptan imágenes, en futuro, podríamos manejarlo de otra forma.
    if datos_solicitud.imagen and datos_solicitud.tipoImagen:
        user_content.append(datos_solicitud.prompt)
    else:
        user_content.append(datos_solicitud.prompt)

    # Unimos el contenido en una sola cadena para el mensaje del usuario
    messages.append({
        "role": "user",
        "content": "\n".join(user_content)
    })

    return messages


def _llamar_api_sdk(messages: list[dict], system_prompt: str, modelo_id:str)->str:
    """
    Realiza la llamada a la API de Groq utilizando el SDK.
    """
    full_messages = [
        {"role": "system", "content": system_prompt}
    ] + messages

    try:
        completion = groq_client.chat.completions.create(
            model=modelo_id,
            messages=full_messages,
            temperature=0.7
        )

        return completion.choices[0].message.content.strip()

    except Exception as e:
        raise Exception(f"Error al usar el SDK de Groq con el modelo {modelo_id}. Detalle: {e}")