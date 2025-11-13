# app.py - Servidor de prueba de Flask para ChefGPT

from flask import Flask, jsonify
from flask_cors import CORS

# 1. Inicializar la aplicación Flask
app = Flask(__name__)

# 2. Configurar CORS (Cross-Origin Resource Sharing)
# Esto es ESENCIAL para permitir que tu frontend (Next.js en localhost:3000)
# pueda hacer peticiones a tu backend (Flask en localhost:5000)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})


# 3. Ruta "Raíz" (para probar en el navegador)
# Esta es una ruta simple para ver si el servidor está vivo.
@app.route('/')
def home():
    return "¡El servidor Backend de ChefGPT (Flask) está funcionando!"


# 4. Ruta de API de Prueba (para probar la conexión con el frontend)
# Esta es una ruta de API real que devuelve datos en formato JSON.
@app.route('/api/test', methods=['GET'])
def api_test():
    # jsonify convierte un diccionario de Python en una respuesta JSON
    # que tu frontend de Next.js podrá entender fácilmente.
    return jsonify(message="¡Conexión con la API de ChefGPT exitosa! 🔥")


# 5. Punto de entrada para ejecutar el servidor
if __name__ == '__main__':
    # debug=True hace que el servidor se reinicie automáticamente
    # cada vez que guardas un cambio en el código.
    # port=5000 es el puerto donde correrá el backend.
    app.run(debug=True, port=5000)

    