import os
import requests
import json
from dotenv import load_dotenv
from app.models.SolicitudReceta import SolicitudReceta
from app.models.Especificaciones import Especificaciones
from app.models.Receta import Receta

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
Eres ChefGPT. Responde **solo** con un JSON válido que represente una receta especificada en el formato de esta clase:

class Receta:
    def __init__(self, nombrePlato, ingredientes, pasos, especificaciones):
        self.nombrePlato = nombrePlato
        self.ingredientes = ingredientes
        self.pasos = pasos
        self.especificaciones = especificaciones

## FORMATO DE RESPUESTA (OBLIGATORIO)

{{
  "nombrePlato": "string",
  "ingredientes": ["ing1", "ing2"],
  "pasos": ["paso 1", "paso 2"],
  "especificaciones": "Texto opcional"
}}

**ATENCIÓN:** El JSON debe ser el único contenido de tu respuesta.
**PROHIBIDO:** No agregues NADA (texto, explicaciones, saludos, bloques de código markdown como ```json o ```) antes o después del JSON.  
Solo responde con el JSON.

## SI EL PROMPT O LA IMAGEN NO CONTIENEN COMIDA
Responde únicamente con el string: error.

## INFORMACIÓN DEL USUARIO
Prompt: "{comida}"

## ESPECIFICACIONES (SI AL MENOS UNA ESTÁ DEFINIDA)
Tipo de dieta: "{tipo_dieta}"
Objetivo: "{objetivo}"
Restricciones: "{restricciones}"
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

        if response.status_code != 200:
            return f"Error de Google ({response.status_code}): {response.text}"

        resultado = response.json()

        # Extraer texto devuelto por la IA
        texto = resultado['candidates'][0]['content']['parts'][0]['text'].strip()

        json_str = estraerJSON(texto=texto)

        try:
            json_receta = json.loads(json_str)
        except Exception as e:
            return f"Error al parsear JSON: {e}. Contenido recibido: {texto}"

        # Crear el objeto Receta
        recetaObj = Receta(
            json_receta.get("nombrePlato"),
            json_receta.get("ingredientes"),
            json_receta.get("pasos"),
            json_receta.get("especificaciones", '')
        )

        return recetaObj

    except Exception as e:
        return f"Error de conexión: {str(e)}"


def estraerJSON(texto):
    inicio = texto.find("{")
    fin = texto.rfind("}") + 1

    if inicio == -1 or fin == -1:
        return f"Error: La IA no devolvió un JSON válido. Respuesta: {texto}"

    return texto[inicio:fin]