import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

def generar_receta_ia(datos_solicitud):
    """
    Consulta a Gemini usando peticiones HTTP directas (sin SDK).
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return "Error: Falta la API Key en el archivo .env"

    # 1. Obtener datos
    comida = datos_solicitud.get('comida', '')
    modelo_id = datos_solicitud.get('modeloIASeleccionado', 'gemini-1.5-flash')
    
    # URL oficial de la API REST de Google
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo_id}:generateContent?key={api_key}"

    # 2. Preparar el Prompt (Instrucciones)
    prompt_sistema = (
        "Eres ChefGPT. Responde SOLO con una receta detallada en español sobre: " + comida + ". "
        "Si no es comida, di que no puedes ayudar. Estructura la respuesta con Título, Ingredientes y Pasos."
    )

    # 3. Construir el cuerpo de la petición (JSON)
    payload = {
        "contents": [{
            "parts": [{"text": prompt_sistema}]
        }]
    }
    
    headers = {'Content-Type': 'application/json'}

    try:
        # 4. Enviar la carta (POST)
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        
        # Verificar si salió bien (Código 200)
        if response.status_code == 200:
            resultado = response.json()
            # Extraer el texto de la respuesta compleja de Google
            texto_receta = resultado['candidates'][0]['content']['parts'][0]['text']
            return texto_receta
        else:
            return f"Error de Google ({response.status_code}): {response.text}"

    except Exception as e:
        return f"Error de conexión: {str(e)}"