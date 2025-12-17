from youtube_transcript_api import YouTubeTranscriptApi
import re

youtube_transcript_api = YouTubeTranscriptApi()
def obtener_transcripcion(video_id: str) -> str:
    # Obtener la transcripción (lista de diccionarios)
    try:
        fetched_transcript = youtube_transcript_api.fetch(video_id, languages=['es'])
    except Exception as e:
        print(f"Error al obtener la transcripción: {e}")
        return ""

    # comprensión de lista para extraer el texto de cada snippet.
    textos_individuales = [snippet.text for snippet in fetched_transcript]

    # unir la lista de textos en una sola cadena con espacios.
    texto_unido = " ".join(textos_individuales)

    # obtener solo alfanuméricos sin puntos ni comas.
    texto_limpio_parcial = re.sub(r'[^\w\sáéíóúñÁÉÍÓÚÑ]', '', texto_unido)

    # eliminar múltiples espacios por uno solo (opcional, pero recomendado para limpieza)
    texto_final = re.sub(r'\s+', ' ', texto_limpio_parcial).strip()

    return texto_final