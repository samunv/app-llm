import requests
import json
from dotenv import load_dotenv
import os
from app.models.VideoInfo import VideoInfo
load_dotenv()
api_key = os.getenv("YT_API_KEY")

def obtener_video_youtube(busqueda: str)->VideoInfo | None:
    if not api_key:
        print("Falta la API Key de YouTube en el archivo .env")
        return None
    else:
        url_yt_api_search = "https://www.googleapis.com/youtube/v3/search"

        busqueda_receta = busqueda
        if "receta" not in busqueda.lower():
            busqueda_receta = "receta " + busqueda

        params = {
        'part': 'snippet',
        'q': busqueda_receta,
        'type': 'video',
        'maxResults': 1,
        'key': api_key
        }
        response = requests.get(url_yt_api_search, params=params)

        # Procesar la respuesta JSON
        if response.status_code == 200:
            data = response.json()

            print(f"Resultados de la búsqueda: '{busqueda_receta}'\n")
            for item in data.get('items', []):
                video_id = item['id']['videoId']
                titulo = item['snippet']['title']
                miniatura_url = item['snippet']['thumbnails']['high']['url']
                nombre_canal = item['snippet']['channelTitle']
                print(f"{video_id} | {titulo} | {miniatura_url} | {nombre_canal}")
                return VideoInfo(video_id, titulo, miniatura_url, nombre_canal)

        else:
            print(f"Error en la petición: {response.status_code}")
            print(response.json())
            return None