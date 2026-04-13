import os
import json

from app.models.SolicitudReceta import SolicitudReceta
from app.utils import obtener_instrucciones_generador_recetas, extraer_formato_respuesta
from app.config.groq_client import respuesta_cliente_groq
from app.crewai_module.obtener_receta_jerarquica_service import obtener_receta_jerarquica
from app.function_calling_service import fc_clasificar_solicitud


def generar_respuesta_ia(datos_solicitud: SolicitudReceta = {}, fuente_info: str = ""):
    messages = _obtener_messages_con_historial(datos_solicitud=datos_solicitud)

    # ── FC 1: clasificar_solicitud ─────────────────────────────────────────────
    # Usamos Function Calling para clasificar el prompt del usuario en lugar
    # de una clasificación manual por keywords. El LLM decide si es una
    # petición de receta, una pregunta de seguimiento o algo no relacionado.
    clasificacion = fc_clasificar_solicitud(datos_solicitud.prompt)
    categoria = clasificacion.get("categoria", "otro")

    if categoria == "seguimiento":
        print("[api_model_service] FC1 → seguimiento. Usando SDK directo.")
        return _llamar_api_sdk(
            messages=messages,
            system_prompt="",
            modelo_id=datos_solicitud.modeloIASeleccionado
        )

    if categoria != "receta":
        return "Si quieres una receta, dime el nombre del plato que quieres preparar."

    # ── Lanzar Crew Jerárquica ─────────────────────────────────────────────────
    print("[api_model_service] FC1 → receta. Lanzando Crew Jerárquica.")
    respuesta_crew = obtener_receta_jerarquica(plato=datos_solicitud.prompt)

    if respuesta_crew is None:
        print("[api_model_service] Crew sin resultado. Fallback al SDK.")
        system_prompt = obtener_instrucciones_generador_recetas(
            prompt=datos_solicitud.prompt,
            especificaciones=datos_solicitud.especificaciones,
            fuente_info=fuente_info
        )
        return _llamar_api_sdk(
            messages=[],
            system_prompt=system_prompt,
            modelo_id=datos_solicitud.modeloIASeleccionado
        )

    return extraer_formato_respuesta(respuesta=respuesta_crew)


def _obtener_messages_con_historial(datos_solicitud: SolicitudReceta):
    messages = []
    for mensaje_ia in datos_solicitud.historial:
        role = "assistant" if mensaje_ia["role"] == "model" else "user"
        text = mensaje_ia["parts"][0]["text"]
        messages.append({"role": role, "content": text})
    messages.append({"role": "user", "content": datos_solicitud.prompt})
    return messages


def _llamar_api_sdk(messages: list[dict], system_prompt: str, modelo_id: str) -> str:
    return respuesta_cliente_groq(
        messages=messages,
        system_prompt=system_prompt,
        modelo_id=modelo_id
    )
