#pip install chromadb
import chromadb
from dotenv import load_dotenv
from groq import Groq # Importamos la clase Groq
import os

load_dotenv()
api_key = os.getenv("CHROMADB_CLOUD_API_KEY") 

try:
    chroma_client = chromadb.CloudClient(
        api_key=api_key,
        tenant='0e0f2318-0f11-4f70-af67-73edbc2d2d1a',
        database='chefgpt'
)

except Exception as e:
    print(f"Error al inicializar el cliente de ChromaDB Cloud: {e}")
    groq_client = None

coleccion_transcripciones_de_yt = chroma_client.get_or_create_collection(name="transcripciones_de_yt")


