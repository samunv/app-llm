from app.rutas import app
from flask_cors import CORS

# Permitir peticiones solo desde tu frontend (localhost:3000)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

if __name__ == '__main__':
    print("🔥 Servidor ChefGPT (Python) corriendo en http://127.0.0.1:5000")
    app.run(debug=True, port=5000)