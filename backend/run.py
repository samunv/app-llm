from flask import Flask, jsonify
# 1. Inicializar la aplicación Flask
app = Flask(__name__)

# 5. Punto de entrada para ejecutar el servidor
if __name__ == '__main__':
    # debug=True hace que el servidor se reinicie automáticamente
    # cada vez que guardas un cambio en el código.
    # port=5000 es el puerto donde correrá el backend.
    app.run(debug=True, port=5000)
