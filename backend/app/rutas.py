# app.py - Servidor de prueba de Flask para ChefGPT

from flask import Flask, jsonify
from flask_cors import CORS
from run import app


# 2. Configurar CORS
# Para permitir peticiones de Next.js en localhost:3000
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})


# 3. Ruta (para probar en el navegador)
# Esta es una ruta simple para ver si el servidor está vivo.
@app.route('/')
def home():
    return "¡El servidor Backend de ChefGPT (Flask) está funcionando!"


# 4. Ruta de API de Prueba (para probar la conexión con el frontend)
# Esta es una ruta de API real que devuelve datos en formato JSON.
@app.route('/api/obtener-receta', methods=['POST'])
def api_test():
    # jsonify convierte un diccionario de Python en una respuesta JSON
    # que tu frontend de Next.js podrá entender fácilmente.
    return jsonify(message="¡Conexión con la API de ChefGPT exitosa! 🔥")
