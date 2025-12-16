from youtube_transcript_api import YouTubeTranscriptApi

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
    
    # 3. UNIR: Unir la lista de textos en una sola cadena con espacios.
    return " ".join(textos_individuales)