import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

def generar_receta_ia(datos_solicitud):
    if not api_key:
        return "Error: Falta la API Key en el archivo .env"

    modelo_id = datos_solicitud.get('modeloIASeleccionado', 'gemini-1.5-flash')
    imagen = datos_solicitud.get('imagen', '')

    prompt = obtenerPrompt(datos_solicitud)
    payloadFinal = obtenerPayloadFinal(prompt, imagen)

    return obtenerRespuestaIA(payloadFinal, modelo_id, api_key)


def obtenerPrompt(datos_solicitud):
    comida = datos_solicitud.get('comida', '')
    especificaciones = datos_solicitud.get('especificaciones', {})

    tipo_dieta = especificaciones.get('tipo_dieta', '')
    restricciones = especificaciones.get('restricciones', '')
    objetivo = especificaciones.get('objetivo', '')

    return (
        f"Eres ChefGPT. Responde SOLO con una receta detallada en español sobre: {comida} "
        f"con estas especificaciones del usuario si al menos una está definida. "
        f"Tipo de dieta: {tipo_dieta}, Objetivo: {objetivo}, Restricciones: {restricciones}. "
        "Si no es comida, di que no puedes ayudar. "
        "Estructura la respuesta con Título, Ingredientes y Pasos. "
        "Incluye un apartado de Especificaciones si hay alguna definida. "
        "Formato markdown: título del plato '#', subtítulos '###'."
    )


def obtenerPayloadFinal(prompt, imagen=""):
    if imagen:
        payloadFinal = {
            "contents": [
                {
                    "parts": [
                        {"inline_data": {"data": imagen, "mime_type": "image/jpeg"}},
                        {"text": prompt}
                    ]
                }
            ]
        }
    else:
        payloadFinal = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ]
        }
    return payloadFinal


def obtenerRespuestaIA(payloadFinal, modelo_id, api_key):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo_id}:generateContent?key={api_key}"
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payloadFinal))
        if response.status_code == 200:
            resultado = response.json()
            texto_receta = resultado['candidates'][0]['content']['parts'][0]['text']
            return texto_receta
        else:
            return f"Error de Google ({response.status_code}): {response.text}"
    except Exception as e:
        return f"Error de conexión: {str(e)}"
