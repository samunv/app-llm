from flask import Flask, request, jsonify, make_response
from app.api_model_service import generar_respuesta_ia
from app.models.Especificaciones import Especificaciones
from app.models.SolicitudReceta import SolicitudReceta
from app.local_service import generar_respuesta_ia_local
from app.rate_limiter import rate_limiter
from app.models.Receta import Receta
from app.youtube_search_api_service import obtener_video_youtube
from app.models.VideoInfo import VideoInfo
import uuid
from app.procesar_receta_yt_service import generar_respuesta_yt_video_url
from app.imagenes_service import generar_respuesta_ia_imagen

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


@app.route('/api/ia-video-yt', methods=['POST'])
@rate_limiter.limit("15 per minute")
def procesar_solicitud_video_yt():
    try:
        datos = request.get_json()
        modelo_seleccionado = "llama-3.3-70b-versatile"
        especificacionesObj = Especificaciones(**datos.get("especificaciones", {}))
        solicitudRecetaObj = SolicitudReceta(
            prompt=datos.get('prompt', ''),
            modeloIASeleccionado=modelo_seleccionado,
            especificaciones=especificacionesObj or Especificaciones(),
            historial=datos.get('historial', []),
        )
        print(f"Controller >> LLegada de datos: Especificaciones-> {especificacionesObj.tipo_dieta}, {especificacionesObj.ingredientes_disponibles}")
        response = make_response(_generar_respuesta_yt_video_url(solicitudReceta=solicitudRecetaObj)) 
        _verificar_token_cookies(response=response)
        return response
    except Exception as e:
        print(f"Error en controller: {str(e)}")
        response = make_response(jsonify({"error": str(e), "estado": "error"}))
        _verificar_token_cookies(response=response)
        return response
    

@app.route('/api/ia-imagenes', methods=['POST'])
@rate_limiter.limit("15 per minute")
def procesar_solicitud_imagenes():
    try:
        datos = request.get_json()
        especificacionesObj = Especificaciones(**datos.get("especificaciones", {}))
        solicitudRecetaObj = SolicitudReceta(
            imagen=datos.get('imagen', ''),
            tipoImagen=datos.get('tipoImagen',''),
            especificaciones=especificacionesObj or Especificaciones(),
        )
        response = make_response(
            _json_respuesta(
                generar_respuesta_ia_imagen(
                    imagen_base64=solicitudRecetaObj.imagen, 
                    tipoImagen=solicitudRecetaObj.tipoImagen, 
                    especificaciones=solicitudRecetaObj.especificaciones
                )
            ) 
        )
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
    return _json_respuesta(respuesta=respuesta_ia, video=video)

def _generar_respuesta_ia(solicitudRecetaObj: SolicitudReceta) -> str:
    return generar_respuesta_ia(datos_solicitud=solicitudRecetaObj)

def _generar_respuesta_yt_video_url(solicitudReceta: SolicitudReceta)-> str|None:
    respuesta = ""
    if solicitudReceta.prompt.lower().startswith("https://www.youtube.com/watch?v="):
        respuesta = generar_respuesta_yt_video_url(datos_solicitud=solicitudReceta)
    else:
        respuesta = "La URL que has envíado no es válida o no es la esperada. Debe empezar por 'https://www.youtube.com/watch?v='."
    return _json_respuesta(respuesta=respuesta, video=None)


def _obtener_video(respuesta_ia: Receta | str) -> VideoInfo | None:
    if isinstance(respuesta_ia, Receta):
        return obtener_video_youtube(respuesta_ia.nombrePlato)
    return None


def _json_respuesta(respuesta: Receta | str, video: VideoInfo = None):

    if isinstance(respuesta, Receta):
        respuesta_dict = respuesta.model_dump() 
        tipo_respuesta = "receta"
    elif isinstance(respuesta, dict) and "error" in respuesta:
        # Caso de error {"error": "..."}
        respuesta = respuesta["error"]
        tipo_respuesta = "error"
    else:
        tipo_respuesta = "chat"
        
    return jsonify({
            "respuesta": respuesta_dict if isinstance(respuesta, Receta) else respuesta,
            "tipo": tipo_respuesta,
            "estado": "exito",
            "video": video.to_dict() if video else None
        })
