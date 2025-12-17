
from app.utils import extraer_video_id
from app.youtube_transcript_service import obtener_transcripcion
from app.youtube_video_service import obtener_video_youtube_mediante_videoID
from app.models.VideoInfo import VideoInfo
from app.models.Receta import Receta
from app.models.Especificaciones import Especificaciones
from app.youtube_search_api_service import obtener_video_youtube
from app.clasificador_service import clasificar_video
from app.rag_service.rag_transcripciones_service import obtener_receta_semantica_de_transcripciones

def generar_respuesta_yt_video_url(prompt: str, especificaciones: Especificaciones = {})-> str:
    if prompt.lower().startswith("https://www.youtube.com/watch?v="):
        # TODO: Implementar generación de respuesta basada en video de YouTube
        # TODO: requerirá que haya un agente que estudie si el video es una receta
        # TODO: otro agente generará una receta basada en la transcripción del video.
        video_estatus = _verificar_video_existente(prompt=prompt)

        if not video_estatus:
                return "No existe el vídeo con la URL envíada."

        if isinstance(video_estatus, str):
            return video_estatus 

        video = video_estatus

        # Obtener transcripción
        transcripcion = _obtener_transcripcion(video_id=video.video_id)

        # Clasificar si el video se trata de una receta o no:
        if not clasificar_video(titulo_video=video.titulo, transcripcion=transcripcion):
            return "El vídeo no se trata de una receta válida. Por favor, pega el enlace de un vídeo válido para obtener la receta."

        # Obtener receta a partir de la transcripcion
        # receta: Receta = generar_receta_de_yt()
        # verificar que receta sea del tipo receta para enviar
        receta_semantica = obtener_receta_semantica_de_transcripciones(video_info=video, transcripcion=transcripcion)

        # Por ahora solo devolvemos los docs obtenidos
        return receta_semantica
    else:
        return "La URL no es válida o no empieza por 'https://www.youtube.com/watch?v='."

def _verificar_video_existente(prompt:str)->VideoInfo|None:
    video_id = extraer_video_id(prompt)
    if not video_id:
        return None

    video: VideoInfo | None = obtener_video_youtube_mediante_videoID(video_id)

    if not video:

        return "El vídeo envíado no es válido. Ten en cuenta que solamente se aceptan videos de YouTube cuya duración sea como máximo de 30 minutos y en español."
    return video



def _obtener_transcripcion(video_id: str)-> str:
    # TODO: Este método se borrará cuando se implemente el agente de video completo.
    # Actualmente solo extrae la transcripción de un video de YouTube si la URL es válida.
    transcripcion: str = obtener_transcripcion(video_id)
    if transcripcion:
        return transcripcion
    else:
        return f"El vídeo envíado es: {video_id}. No tiene transcripción disponible o no es en Español."


# def _obtener_video(respuesta_ia: Receta | str) -> VideoInfo | None:
#     if isinstance(respuesta_ia, Receta):
#         return obtener_video_youtube(respuesta_ia.nombrePlato)
#     return None

def _generar_y_obtener_receta_de_yt():
    return ""