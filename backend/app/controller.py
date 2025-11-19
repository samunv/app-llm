from flask import Flask, request, jsonify
from app.service import generar_receta_ia
from app.models.Especificaciones import Especificaciones
from app.models.SolicitudReceta import SolicitudReceta

app = Flask(__name__)

# Endpoint POST
@app.route('/api/ia', methods=['POST'])
def procesar_solicitud():
    try:
        # Recibimos el JSON del frontend (SolicitudReceta)
        datos = request.get_json()
        print("📩 Solicitud recibida:", datos) # Log para ver en consola

        # Convertir el dict a Objetos
        especificacionesObj = Especificaciones(**datos.get("especificaciones", {})) # rellenar los parametros
        solicitudRecetaObj = SolicitudReceta(
            comida=datos.get('comida', ''),
            modeloIASeleccionado=datos.get('modeloIASeleccionado', ''),
            imagen=datos.get('imagen', ''),
            tipoImagen=datos.get('tipoImagen',''),
            especificaciones=especificacionesObj or Especificaciones(),
        )

        # Llamamos a la IA
        respuesta_ia = generar_receta_ia(solicitudRecetaObj)

        # Log por si hay errores
        print(respuesta_ia)

        if hasattr(respuesta_ia, "to_dict"):
            respuesta_ia = respuesta_ia.to_dict()

        # Devolvemos la respuesta al frontend
        return jsonify({
            "respuesta": respuesta_ia,
            "estado": "exito"
        })

    except Exception as e:
        return jsonify({"error": str(e), "estado": "error"}), 500