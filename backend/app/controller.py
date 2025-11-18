from flask import Flask, request, jsonify
from app.service import generar_receta_ia

app = Flask(__name__)

# Definimos la ruta POST
@app.route('/api/ia', methods=['POST'])
def procesar_solicitud():
    try:
        # Recibimos el JSON del frontend (SolicitudReceta)
        datos = request.get_json()
        
        print("📩 Solicitud recibida:", datos) # Log para ver en consola

        # Llamamos a la IA
        respuesta_ia = generar_receta_ia(datos)

        # Devolvemos la respuesta al frontend
        return jsonify({
            "respuesta": respuesta_ia,
            "estado": "exito"
        })

    except Exception as e:
        return jsonify({"error": str(e), "estado": "error"}), 500