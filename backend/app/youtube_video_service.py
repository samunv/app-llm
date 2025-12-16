import requests
from isodate import parse_duration
# Asegúrate de tener estas importaciones:
from app.models.VideoInfo import VideoInfo
import os, json
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("YT_API_KEY")

def obtener_video_youtube_mediante_videoID(video_id: str) -> VideoInfo | None:
    if not api_key:
        print("Falta la API Key de YouTube en el archivo .env")
        return None
    
    url_yt_api_videos = "https://www.googleapis.com/youtube/v3/videos"

    params = {
        'id': video_id,
        # Necesitamos el snippet para el título/canal, contentDetails para la duración
        'part': 'snippet,contentDetails', 
        'key': api_key
    }

    try:
        # Realizar la solicitud HTTP
        response = requests.get(url_yt_api_videos, params=params)
        response.raise_for_status() 
        data = response.json()
        # Llamar a la función de procesamiento con los datos JSON
        return _procesar_datos_video(data, video_id)

    except requests.exceptions.RequestException as e:
        print(f"Error HTTP o de conexión con la API de YouTube: {e}")
        return None
    except json.JSONDecodeError:
        print("Error al decodificar la respuesta JSON.")
        return None


def _procesar_datos_video(data: dict, video_id: str) -> VideoInfo | None:
    # Renombré la función para reflejar mejor su propósito
    if not data or not data.get('items'):
        print(f"Advertencia: Video ID '{video_id}' no encontrado o respuesta vacía.")
        return None
        
    item = data['items'][0]
    snippet = item['snippet']
    contentDetails = item['contentDetails']

    duracion_segundos = _obtener_duracion_video_en_segundos(contentDetails)
    
    # 30 minutos 
    DURACION_MAXIMA_SEGUNDOS = 1800 

    if not _comprobar_duracion_video(duracion_segundos, DURACION_MAXIMA_SEGUNDOS):
        return None

    return VideoInfo(
        video_id=video_id,
        titulo=snippet.get('title'),
        nombre_canal=snippet.get('channelTitle'),

    )

def _obtener_duracion_video_en_segundos(contentDetails: dict) -> float:
    """Extrae la duración en formato ISO 8601 y la convierte a segundos."""
    duracion_iso = contentDetails.get('duration', 'PT0S')
    try:
        duration_timedelta = parse_duration(duracion_iso)
        return duration_timedelta.total_seconds()
    except Exception as e:
        print(f"Error al parsear duración ISO '{duracion_iso}': {e}")
        return 0.0

# _comprobar_duracion_video no necesita cambios
def _comprobar_duracion_video(duracion_video: float, duracion_maxima: float) -> bool:
    if duracion_video <= duracion_maxima:
        return True
    else:
        print(f"El video excede la duración máxima permitida de {duracion_maxima} segundos.")
        return False