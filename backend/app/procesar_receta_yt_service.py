
from app.utils import extraer_video_id
from app.youtube_transcript_service import obtener_transcripcion
from app.youtube_video_service import obtener_video_youtube_mediante_videoID
from app.models.VideoInfo import VideoInfo
from app.models.SolicitudReceta import SolicitudReceta
from app.models.Receta import Receta

from app.crewai_module.procesar_receta_yt import procesar_receta_yt
from app.rag_service.rag_transcripciones_service import  registrar_transcripcion_si_no_existe


def generar_respuesta_yt_video_url(datos_solicitud: SolicitudReceta) -> Receta | str:
    video = _verificar_video_existente(prompt=datos_solicitud.prompt)

    if not video:
        return "No existe el vídeo o es inválido. Asegúrate de enviar una URL de YouTube correcta."

    transcripcion = _obtener_transcripcion(video.video_id)

    # Verificamos si el video pasa el primer filtro de ser una receta:
    if not es_video_receta(transcripcion):
        return "El vídeo no parece ser una receta válida. Asegúrate de que el video tenga instrucciones claras de cocina, ingredientes y pasos de preparación."

    # Registramos la transcripción completa en ChromaDB si no existe, para optimizar futuras consultas
    registrar_transcripcion_si_no_existe(video_info=video, transcripcion=transcripcion)

    # Ejecutamos la Crew con el contenido optimizado
    resultado = procesar_receta_yt(titulo=video.titulo, video_id=video.video_id)

    return resultado if resultado else "El vídeo no es una receta válida."


def es_video_receta(transcripcion: str) -> bool:
    if not transcripcion or len(transcripcion.strip()) < 50:
        return False
    

    #Solo analizamos los primeros 2000 caracteres
    # Las recetas normalmente mencionan ingredientes y contexto al inicio
    texto = transcripcion[:2000].lower()

    # Palabras fuertes: si aparece cualquiera, casi seguro es receta
    palabras_fuertes = [
        "ingredientes", "receta", "preparación", "elaboración",
        "cucharada", "cucharadita", "gramos", "litros", "mililitros",
        "precalentar", "hornear", "hervir", "sofreír", "saltear",
        "picar", "mezclar", "batir", "amasar", "marinar"
    ]

    # Palabras débiles: necesita varias para confirmar
    palabras_debiles = [
        "cocinar", "preparar", "cocer", "añadir", "agregar",
        "poner", "echar", "calentar", "enfriar", "servir",
        "minutos", "horno", "sartén", "olla", "cazuela"
    ]

    hits_fuertes = sum(1 for p in palabras_fuertes if p in texto)
    hits_debiles = sum(1 for p in palabras_debiles if p in texto)

    # Es receta si: al menos 1 palabra fuerte, o 3+ palabras débiles
    return hits_fuertes >= 1 or hits_debiles >= 3


def _verificar_video_existente(prompt:str)->VideoInfo|None:
    video_id = extraer_video_id(prompt)
    if not video_id:
        return None

    video: VideoInfo | None = obtener_video_youtube_mediante_videoID(video_id)

    if not video:
        return None
    return video



def _obtener_transcripcion(video_id: str)-> str:
    # Solo extrae la transcripción de un video de YouTube si la URL es válida.
    transcripcion: str = obtener_transcripcion(video_id)
    if transcripcion:
        return transcripcion
    else:
        return f"El vídeo envíado es: {video_id}. No tiene transcripción disponible o no es en Español."
