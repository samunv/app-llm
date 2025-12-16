from flask import Flask, request, jsonify, make_response
# from app.gemini_service import generar_respuesta_ia
from app.api_model_service import generar_respuesta_ia
from app.models.Especificaciones import Especificaciones
from app.models.SolicitudReceta import SolicitudReceta
from app.local_service import generar_respuesta_ia_local
from app.rate_limiter import rate_limiter
from app.models.Receta import Receta
from app.youtube_search_api_service import obtener_video_youtube
from app.models.VideoInfo import VideoInfo
import uuid
from app.utils import filtrar_palabras_clave, extraer_video_id
from app.youtube_transcript_service import obtener_transcripcion
from app.youtube_video_service import obtener_video_youtube_mediante_videoID

app = Flask(__name__)

rate_limiter.init_app(app)

@app.route('/api/ia', methods=['POST'])
@rate_limiter.limit("15 per minute")
def procesar_solicitud():
    try:
        datos = request.get_json()
        #modeloSeleccionado = datos.get('modeloIASeleccionado', '')
        especificacionesObj = Especificaciones(**datos.get("especificaciones", {}))
        solicitudRecetaObj = SolicitudReceta(
            prompt=datos.get('prompt', ''),
            modeloIASeleccionado=datos.get('modeloIASeleccionado', ''),
            imagen=datos.get('imagen', ''),
            tipoImagen=datos.get('tipoImagen',''),
            especificaciones=especificacionesObj or Especificaciones(),
            historial=datos.get('historial', []),
        )
        response = make_response(_generar_y_obtener_respuesta(solicitudRecetaObj=solicitudRecetaObj)) 
        _verificar_token_cookies(response=response)
        return response
    except Exception as e:
        print(f"Error en controller: {str(e)}")
        response = make_response(jsonify({"error": str(e), "estado": "error"}))
        _verificar_token_cookies(response=response)
        return response



def _verificar_token_cookies(response):
    token = request.cookies.get("client_token")
    if not token:
        token = str(uuid.uuid4())
    response.set_cookie(
        "client_token", 
        token,
        httponly=True,
        samesite="Lax",
        path="/"
    )



def _generar_y_obtener_respuesta(solicitudRecetaObj: SolicitudReceta):
    respuesta_ia = _generar_respuesta_ia(solicitudRecetaObj)
    video = _obtener_video(respuesta_ia=respuesta_ia)
    return _json_respuesta(respuesta_ia=respuesta_ia, video=video)


def _generar_respuesta_ia(solicitudRecetaObj: SolicitudReceta) -> str:

    if solicitudRecetaObj.prompt.lower().startswith("https://www.youtube.com/watch?v="):
            # TODO: Implementar generación de respuesta basada en video de YouTube
            # TODO: requerirá que haya un agente que estudie si el video es una receta
            # TODO: otro agente generará una receta basada en la transcripción del video.
            return _obtener_transcripcion(solicitudRecetaObj.prompt)
    else:
        #return generar_respuesta_ia_local(solicitudRecetaObj)
            return generar_respuesta_ia(solicitudRecetaObj)
 
def _obtener_transcripcion(prompt: str)-> str | None:
    # TODO: Este método se borrará cuando se implemente el agente de video completo.
    # Actualmente solo extrae la transcripción de un video de YouTube si la URL es válida.
    video_id = extraer_video_id(prompt)
    if not video_id:
        return "El vídeo envíado no existe o la URL no es válida."

    video: VideoInfo | None = obtener_video_youtube_mediante_videoID(video_id)

    if not video:
        return "El vídeo envíado no es válido. Ten en cuenta que solamente se aceptan videos de YouTube cuya duración sea como máximo de 30 minutos."
    
    
    transcripcion: str = obtener_transcripcion(video_id)
    if transcripcion:
        return transcripcion
    else:
        return f"El vídeo envíado es: {video_id}. No tiene transcripción disponible."


def _obtener_video(respuesta_ia: Receta | str) -> VideoInfo | None:
    if isinstance(respuesta_ia, Receta):
        return obtener_video_youtube(respuesta_ia.nombrePlato)
    return None


def _json_respuesta(respuesta_ia: Receta | str, video: VideoInfo = None):

    if isinstance(respuesta_ia, Receta):
        respuesta_ia_dict = respuesta_ia.model_dump() 
        tipo_respuesta = "receta"
    elif isinstance(respuesta_ia, dict) and "error" in respuesta_ia:
        # Caso de error {"error": "..."}
        respuesta_ia = respuesta_ia["error"]
        tipo_respuesta = "error"
    else:
        tipo_respuesta = "chat"
        
    return jsonify({
            "respuesta": respuesta_ia_dict if isinstance(respuesta_ia, Receta) else respuesta_ia,
            "tipo": tipo_respuesta,
            "estado": "exito",
            "video": video.to_dict() if video else None
        })
