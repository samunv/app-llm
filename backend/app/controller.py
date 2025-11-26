from flask import Flask, request, jsonify, make_response
from app.gemini_service import generar_respuesta_ia
from app.models.Especificaciones import Especificaciones
from app.models.SolicitudReceta import SolicitudReceta
from app.local_service import generar_respuesta_ia_local
from app.rate_limiter import rate_limiter
from app.models.Receta import Receta
import uuid

app = Flask(__name__)

rate_limiter.init_app(app)

@app.route('/api/ia', methods=['POST'])
@rate_limiter.limit("15 per minute")
def procesar_solicitud():
    try:
        datos = request.get_json()
        modeloSeleccionado = datos.get('modeloIASeleccionado', '')
        especificacionesObj = Especificaciones(**datos.get("especificaciones", {}))
        solicitudRecetaObj = SolicitudReceta(
            comida=datos.get('comida', ''),
            modeloIASeleccionado=datos.get('modeloIASeleccionado', ''),
            imagen=datos.get('imagen', ''),
            tipoImagen=datos.get('tipoImagen',''),
            especificaciones=especificacionesObj or Especificaciones(),
            historial=datos.get('historial', []),
        )
        response = make_response(_generar_y_obtener_respuesta(modeloSeleccionado=modeloSeleccionado, solicitudRecetaObj=solicitudRecetaObj)) 
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





def _generar_y_obtener_respuesta(modeloSeleccionado: str, solicitudRecetaObj: SolicitudReceta):
    respuesta_ia = ""

    if modeloSeleccionado != "llama3:8b":
        respuesta_ia = generar_respuesta_ia(solicitudRecetaObj)

    else:
        respuesta_ia = generar_respuesta_ia_local(solicitudRecetaObj)

    return _json_respuesta(respuesta_ia=respuesta_ia)






def _json_respuesta(respuesta_ia: Receta | str):

    if hasattr(respuesta_ia, "to_dict"):
        respuesta_ia = respuesta_ia.to_dict()
        tipo_respuesta = "receta"
    elif isinstance(respuesta_ia, dict) and "error" in respuesta_ia:
        # Caso de error {"error": "..."}
        respuesta_ia = respuesta_ia["error"]
        tipo_respuesta = "error"
    else:
        tipo_respuesta = "chat"
        
    return jsonify({
            "respuesta": respuesta_ia,
            "tipo": tipo_respuesta,
            "estado": "exito"
        })
