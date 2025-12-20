
import json
import requests
import os
from dotenv import load_dotenv
from app.models.Receta import Receta

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")


def respuesta_api_gemini(payload: dict[str, any], modelo_id:str)->str|Receta:
    if not api_key:
        return "Falta la API Key en el archivo .env"

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo_id}:generateContent"
    headers = {"Content-Type": "application/json","x-goog-api-key": api_key }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        resultado = response.json()
        return resultado["candidates"][0]["content"]["parts"][0]["text"].strip()
    except Exception as e:
        print(f"Error al llamar Gemini: {e}")
        raise Exception(f"no se ha podido conectar con {modelo_id}. Pruebe en otro momento, o seleccione otro modelo de IA hasta que se resuelva el problema.")
