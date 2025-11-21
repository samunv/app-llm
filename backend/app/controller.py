from flask import Flask, request, jsonify
from app.service import generar_respuesta_ia
from app.models.Especificaciones import Especificaciones
from app.models.SolicitudReceta import SolicitudReceta

app = Flask(__name__)

@app.route('/api/ia', methods=['POST'])
def procesar_solicitud():
    try:
        datos = request.get_json()

        especificacionesObj = Especificaciones(**datos.get("especificaciones", {}))

        solicitudRecetaObj = SolicitudReceta(
            comida=datos.get('comida', ''),
            modeloIASeleccionado=datos.get('modeloIASeleccionado', ''),
            imagen=datos.get('imagen', ''),
            tipoImagen=datos.get('tipoImagen',''),
            especificaciones=especificacionesObj or Especificaciones(),
            historial=datos.get('historial', []),
        )

        # Llamamos al servicio
        respuesta_ia = generar_respuesta_ia(solicitudRecetaObj)

        # Si es objeto Receta, lo pasamos a dict. Si es texto (chat), se queda como texto.
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

    except Exception as e:
        print(f"Error en controller: {str(e)}")
        return jsonify({"error": str(e), "estado": "error"}), 500