import os
import json

from app.models.SolicitudReceta import SolicitudReceta
from app.utils import obtener_instrucciones_generador_recetas, extraer_formato_respuesta
from app.config.groq_client import respuesta_cliente_groq
from app.crewai_module.obtener_receta_jerarquica_service import obtener_receta_jerarquica

def generar_respuesta_ia(datos_solicitud: SolicitudReceta = {}, fuente_info: str = ""):
    # Identificar si es una duda de seguimiento o una petición de receta nueva
    es_seguimiento = _es_pregunta_de_seguimiento(datos_solicitud.prompt)
    messages = _obtener_messages_con_historial(datos_solicitud=datos_solicitud)
    system_prompt = ""

    # Si es seguimiento, vamos DIRECTO al LLM (SDK) para ahorrar recursos
    if es_seguimiento:
        print(" Detectada pregunta de seguimiento. Saltando Crew, usando SDK...")
        return _llamar_api_sdk(messages=messages, system_prompt=system_prompt, modelo_id=datos_solicitud.modeloIASeleccionado)

    if not _es_pregunta_de_receta(datos_solicitud.prompt):
        return "Si quieres una receta, debes incluir al menos la palabra 'receta' + nombre del plato en tu mensaje."

    #  Si pide una receta explícitamente, lanzamos la Crew Jerárquica
    respuesta_crew = obtener_receta_jerarquica(plato=datos_solicitud.prompt)

    # Si la Crew no pudo (None), fallback al SDK como red de seguridad
    if respuesta_crew is None:
        print(" La Crew no devolvió una receta válida. Fallback al SDK...")
        system_prompt = obtener_instrucciones_generador_recetas(
            prompt=datos_solicitud.prompt, 
            especificaciones=datos_solicitud.especificaciones,
            fuente_info=fuente_info)
        return _llamar_api_sdk(messages=[], system_prompt=system_prompt, modelo_id=datos_solicitud.modeloIASeleccionado)

    #Si todo fue bien, devolvemos el JSON de la receta formateado
    return extraer_formato_respuesta(respuesta=respuesta_crew)


def _es_pregunta_de_receta(prompt: str) -> bool:
    indicadores = [
        "receta", "preparar", "prepara", 
        "cómo se hace", "cómo preparar", "enséñame a cocinar", 
        "receta de", "cómo se cocina", "cómo se cocina", "dame una receta",
    ]
    prompt_lower = prompt.lower()
    return any(word in prompt_lower for word in indicadores)

def _es_pregunta_de_seguimiento(prompt: str) -> bool:
    # Solo palabras que REFERENCIAN al pasado
    indicadores = [
        "este", "esa", "anterior", "antes", "anterior", 
        "repite", "dijiste", "esa receta", "la anterior", 
        "sobre eso", "respecto a eso"
    ]
    prompt_lower = prompt.lower()

    if "receta" in prompt_lower:
        return False

    # Si contiene indicadores claros de "memoria de chat", es seguimiento
    if any(word in prompt_lower for word in indicadores):
        return True

    return False

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