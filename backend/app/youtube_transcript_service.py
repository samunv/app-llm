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

    return _limpiar_stopwords(texto_final)

def _limpiar_stopwords(texto: str) -> str:
    cta = [
        "suscríbete", "suscribiros", "dale a like", "enlace en la descripción", 
        "caja de información", "canal", "comenta abajo", "comparte este video",
        "redes sociales", "instagram", "facebook", "tiktok", "clica", "campanita", "gustado", "vídeo", "enseñar", "música"
    ]

    cortesia = [
        "hola", "bienvenidos", "buenos días", "buenas tardes", "buenas noches",
        "saludos", "adiós", "hasta la próxima", "espero que estéis bien",
        "un beso", "un fuerte abrazo", "gracias por estar aquí", "bien", "ustedes", "usted"
    ]

    relleno = [
        "bueno pues", "entonces", "entonces lo que vamos a hacer", 
        "como os decía", "fijaros", "mira", "mirad", "por aquí", 
        "en este caso", "digamos que", "la verdad es que", "básicamente",
        "a continuación"
    ]

    texto_bajo = texto.lower()

    # Aplicar limpieza de frases completas primero (las más largas)
    todas = cta + cortesia + relleno
    for palabra in todas:
        texto_bajo = texto_bajo.replace(palabra, "")

    return texto_bajo