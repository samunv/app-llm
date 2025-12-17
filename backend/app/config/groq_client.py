from dotenv import load_dotenv
from groq import Groq # Importamos la clase Groq
import os

load_dotenv()
api_key = os.getenv("GROQ_API_KEY") 

try:
    groq_client = Groq(api_key=api_key)
except Exception as e:
    print(f"Error al inicializar el cliente Groq: {e}")
    groq_client = None

def respuesta_cliente_groq(messages: list[dict], system_prompt: str, modelo_id:str)->str:
    """
    Realiza la llamada a la API de Groq utilizando el SDK.
    """
    full_messages = [
        {"role": "system", "content": system_prompt}
    ] + messages

    try:
        completion = groq_client.chat.completions.create(
            model=modelo_id or "llama-3.1-8b-instant",
            messages=full_messages,
            temperature=0.7
        )

        return completion.choices[0].message.content.strip()

    except Exception as e:
        raise Exception(f"Error al usar el SDK de Groq con el modelo {modelo_id}. Detalle: {e}")