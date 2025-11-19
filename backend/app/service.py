import os
import requests
import json
from dotenv import load_dotenv
from app.models.SolicitudReceta import SolicitudReceta
from app.models.Especificaciones import Especificaciones

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

def generar_receta_ia(datos_solicitud: SolicitudReceta):
    if not api_key:
        return "Error: Falta la API Key en el archivo .env"

    modelo_id = datos_solicitud.modeloIASeleccionado or 'gemini-2.5-flash'
    imagen = datos_solicitud.imagen or ''
    tipoImagen = datos_solicitud.tipoImagen

    prompt = obtenerPrompt(datos_solicitud)
    payloadFinal = obtenerPayloadFinal(prompt, imagen, tipoImagen=tipoImagen)

    return obtenerRespuestaIA(payloadFinal, modelo_id, api_key)


def obtenerPrompt(datos_solicitud: SolicitudReceta):
    comida = datos_solicitud.comida or ''
    especificaciones = datos_solicitud.especificaciones or Especificaciones()

    tipo_dieta = especificaciones.tipo_dieta or ''
    restricciones = especificaciones.restricciones or ''
    objetivo = especificaciones.objetivo or ''

    return f"""
Eres ChefGPT. RESPONDE **SOLO** con la receta en formato Markdown, sin ningún texto adicional. 
No agregues saludos, confirmaciones ni explicaciones. Si la comida no inluye nada que tenga que ver con comida, imprimirás un error.

## INFORMACIÓN DEL USUARIO
Prompt: "{comida}"
Tipo de dieta: {tipo_dieta}
Objetivo: {objetivo}
Restricciones: {restricciones}
En caso de que exista imagen, si identificas comida en ella, harás una receta solo si el prompt lo pide. Si el prompt pide otra cosa, prevalecerá la comida del prompt(recuerda, siemore que tenga que ver con comida).
Si no identificas comida en la imagen, y el prompt tiene comida, harás caso al prompt. Si ninguna es comida, devolverás un error.


## FORMATO OBLIGATORIO (Markdown)
# Título del plato
## Especificaciones (solo si existen)
## Ingredientes
- ingrediente 1
- ingrediente 2
- ...

## Pasos
1. Paso 1
2. Paso 2
3. ...

No agregues nada fuera de esta estructura.
    """


def obtenerPayloadFinal(prompt, imagen, tipoImagen):
    if imagen and tipoImagen:
        payloadFinal = {
            "contents": [
                {
                    "parts": [
                        {"inline_data": {"data": imagen, "mime_type": tipoImagen}},
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
