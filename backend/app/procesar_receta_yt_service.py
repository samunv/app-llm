
from app.utils import extraer_video_id
from app.youtube_transcript_service import obtener_transcripcion
from app.youtube_video_service import obtener_video_youtube_mediante_videoID
from app.models.VideoInfo import VideoInfo
from app.models.Receta import Receta
from app.youtube_search_api_service import obtener_video_youtube

def generar_respuesta_yt_video_url(prompt: str)-> str|None:
    if prompt.lower().startswith("https://www.youtube.com/watch?v="):
            # TODO: Implementar generación de respuesta basada en video de YouTube
            # TODO: requerirá que haya un agente que estudie si el video es una receta
            # TODO: otro agente generará una receta basada en la transcripción del video.
            return _obtener_transcripcion(prompt)
    else:
        return "La URL no es válida o no empieza por 'https://www.youtube.com/watch?v='."


def _obtener_transcripcion(prompt: str)-> str:
    # TODO: Este método se borrará cuando se implemente el agente de video completo.
    # Actualmente solo extrae la transcripción de un video de YouTube si la URL es válida.
    video_id = extraer_video_id(prompt)
    if not video_id:
        return "El vídeo envíado no existe o la URL no es válida."

    video: VideoInfo | None = obtener_video_youtube_mediante_videoID(video_id)

    if not video:
        return "El vídeo envíado no es válido. Ten en cuenta que solamente se aceptan videos de YouTube cuya duración sea como máximo de 30 minutos y en español."

    transcripcion: str = obtener_transcripcion(video_id)
    if transcripcion:
        return transcripcion
    else:
        return f"El vídeo envíado es: {video_id}. No tiene transcripción disponible o no es en Español."


def _obtener_video(respuesta_ia: Receta | str) -> VideoInfo | None:
    if isinstance(respuesta_ia, Receta):
        return obtener_video_youtube(respuesta_ia.nombrePlato)
    return None