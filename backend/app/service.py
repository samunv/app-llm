import os
import requests
import json
from dotenv import load_dotenv
from app.models.SolicitudReceta import SolicitudReceta
from app.models.Especificaciones import Especificaciones
from app.models.Receta import Receta

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

def generar_respuesta_ia(datos_solicitud: SolicitudReceta):
    if not api_key:
        return "Error: Falta la API Key en el archivo .env"

    modelo_id = datos_solicitud.modeloIASeleccionado or 'gemini-2.5-flash'
    
    if not datos_solicitud.historial:
        return _modo_generar_receta(datos_solicitud, modelo_id)
    else:
        return _modo_chat_continuo(datos_solicitud, modelo_id)


# --- MODO 1: GENERAR RECETA ---
def _modo_generar_receta(datos_solicitud, modelo_id):
    imagen = datos_solicitud.imagen or ''
    tipoImagen = datos_solicitud.tipoImagen
    
    prompt = obtenerPromptReceta(datos_solicitud)
    
    if imagen and tipoImagen:
        contents = [{
            "parts": [
                {"text": prompt},
                {"inline_data": {"data": imagen, "mime_type": tipoImagen}}
            ]
        }]
    else:
        contents = [{"parts": [{"text": prompt}]}]

    payload = { "contents": contents }
    
    texto_respuesta = _llamar_api_gemini(payload, modelo_id)
    
    try:
        json_str = estraerJSON(texto_respuesta)
        json_receta = json.loads(json_str)
        return Receta(
            json_receta.get("nombrePlato"),
            json_receta.get("ingredientes"),
            json_receta.get("pasos"),
            json_receta.get("especificaciones", '')
        )
    except Exception as e:
        return f"Error generando receta: {e}. Respuesta: {texto_respuesta}"


# --- MODO 2: CHAT CONTINUO ---
def _modo_chat_continuo(datos_solicitud, modelo_id):
    contents = datos_solicitud.historial.copy()
    
    # Extraer datos del perfil para inyectarlos en el contexto
    perfil = datos_solicitud.perfilUsuario or {}
    contexto_perfil = ""
    if perfil:
        contexto_perfil = (
            f"\n[SISTEMA: El usuario se llama {perfil.get('nombre', 'Usuario')}. "
            f"Tiene estas alergias/restricciones: {perfil.get('alergias', 'Ninguna')}. "
            f"Sigue esta dieta: {perfil.get('dietaGeneral', 'Ninguna')}. TENLO EN CUENTA.]\n"
        )

    # Añadimos la nueva pregunta del usuario CON el contexto del perfil
    mensaje_usuario = datos_solicitud.comida
    contents.append({
        "role": "user",
        "parts": [{"text": contexto_perfil + mensaje_usuario}]
    })

    payload = { "contents": contents }

    texto_respuesta = _llamar_api_gemini(payload, modelo_id)
    
    return texto_respuesta


# --- FUNCIONES AUXILIARES ---

def _llamar_api_gemini(payload, modelo_id):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo_id}:generateContent?key={api_key}"
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        if response.status_code != 200:
            raise Exception(f"Error Google {response.status_code}: {response.text}")
            
        resultado = response.json()
        return resultado['candidates'][0]['content']['parts'][0]['text'].strip()
    except Exception as e:
        raise e

def obtenerPromptReceta(datos_solicitud: SolicitudReceta):
    comida = datos_solicitud.comida or ''
    especificaciones = datos_solicitud.especificaciones or Especificaciones()
    
    # Datos del Perfil
    perfil = datos_solicitud.perfilUsuario or {}
    info_perfil = (
        f"Nombre: {perfil.get('nombre', 'Usuario')}. "
        f"Alergias: {perfil.get('alergias', 'Ninguna')}. "
        f"Dieta: {perfil.get('dietaGeneral', 'Ninguna')}."
    )

    return f"""
    Eres ChefGPT, un asistente de cocina experto.
    
    ## INFORMACIÓN CRÍTICA DEL USUARIO (RESPETAR SIEMPRE)
    {info_perfil}
    Si la receta pedida contiene alérgenos del usuario, ADVIERTE o SUSTITUYE ingredientes.
    
    Responde **solo** con un JSON válido que represente una receta detallada.
    El formato debe ser EXACTAMENTE este JSON (sin markdown ```json ... ```):
    {{
        "nombrePlato": "Nombre del plato",
        "ingredientes": ["100g de x", "2 cucharadas de y"],
        "pasos": ["Paso 1...", "Paso 2..."],
        "especificaciones": "Consejos extra, advertencias de alérgenos, calorías..."
    }}

    ## PETICIÓN DEL USUARIO
    Prompt: "{comida}"
    Tipo de dieta deseada: "{especificaciones.tipo_dieta}"
    Restricciones adicionales: "{especificaciones.restricciones}"
    Objetivo: "{especificaciones.objetivo}"
    """

def estraerJSON(texto):
    inicio = texto.find("{")
    fin = texto.rfind("}") + 1
    if inicio == -1 or fin == -1:
        # Si falla, a veces el modelo añade texto antes. Intentamos limpiar.
        raise Exception("No se encontró JSON en la respuesta")
    return texto[inicio:fin]