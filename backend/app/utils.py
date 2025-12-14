from app.models.SolicitudReceta import SolicitudReceta
from app.models.Especificaciones import Especificaciones
from app.models.Receta import Receta
from app.models.Receta import Ingrediente
import json
import re
from pydantic import ValidationError, BaseModel


def obtener_instrucciones(datos_solicitud: SolicitudReceta):
    comida = datos_solicitud.comida or ""
    especificaciones = datos_solicitud.especificaciones or Especificaciones()
    tipo_dieta = especificaciones.tipo_dieta or "Ninguna"
    restricciones = especificaciones.restricciones or "Ninguna"
    objetivo = especificaciones.objetivo or "Ninguno"
    ingredientes_disponibles = especificaciones.ingredientes_disponibles or "Ninguno"

    if not _filtrar_palabras_clave(comida):
        return "Debes indicar al usuario amablemente, que solicite una receta de comida."
    else:
        JSON_RECETA_FORMATO = """
{
  "nombrePlato": "Nombre del plato",
  "ingredientes": [
    { "nombre": "Ingrediente 1", "cantidad": "Cantidad 1 (solo número)", "unidadMedida": "Unidad 1" },
    { "nombre": "Ingrediente 2", "cantidad": "Cantidad 2 (solo número)", "unidadMedida": "Unidad 2" }
  ],
  "pasos": ["Paso 1", "Paso 2"],
  "especificaciones": "Texto con restricciones de la dieta o notas especiales."
}
"""

        return f"""
ROL Y OBJETIVO
Eres ChefGPT, un asistente experto en cocina. Tu función principal es generar recetas y responder preguntas sobre la ÚLTIMA receta que generaste.

FORMATO DE RESPUESTA
1. Si el usuario pide una receta, DEVUELVE SOLO el JSON solicitado. NO añadas texto antes ni después.
2. Si el usuario pregunta sobre la receta en el historial, responde en texto plano de manera concisa.
3. Si el usuario pregunta por algo que no es comida o ingredientes, o no hay receta en el historial, pide amablemente que solicite una receta.
4. Todas tus respuestas deben ser siempre en ESPAÑOL (nunca en otro idioma que no sea Español castellano). Si el usuario trata de pedir las cosas en otro idioma, tu responderás en español.


// ESTRUCTURA JSON (OBLIGATORIA)
{JSON_RECETA_FORMATO}

CONTEXTO DE LA SOLICITUD
PROMPT ACTUAL: {comida}
ESPECIFICACIONES DEL USUARIO:
- Dieta: {tipo_dieta}
- Restricciones: {restricciones}
- Objetivo: {objetivo}
- Ingredientes personalizados añadidos: {ingredientes_disponibles}
"""



 
def _filtrar_palabras_clave(texto: str) -> bool:
    palabras_clave = ["receta", "ingredientes", "preparar", "cocinar", "plato", "comida", "cómo hacer", "instrucciones", "pasos"]
    texto_lower = texto.lower()
    if any(palabra in texto_lower for palabra in palabras_clave):
        return True
    return False

def extraer_formato_respuesta(respuesta:str) -> Receta | str:
    try:
        json_str = _extraerJSON(respuesta)
        
        # Intenta validar y construir el objeto Receta directamente desde el JSON
        receta_obj = Receta.model_validate_json(json_str) 
        
        # Si es exitoso (el JSON está limpio y los datos son correctos), devuelve el objeto
        return receta_obj
        
    except ValidationError as e:
        print(f"Error de validación Pydantic (Datos incorrectos): {e}")
        
    except json.JSONDecodeError as e:
        print(f"Error al decodificar JSON (sintaxis mala del LLM): {e}")
        
    except Exception as e:
        print(f"Error desconocido: {e}")


    return respuesta

def _extraerJSON(texto: str) -> str:
    # Versión robusta para aislar el JSON
    texto_limpio = texto.strip().replace("```json", "").replace("```", "").strip()
    inicio = texto_limpio.find('{')
    fin = texto_limpio.rfind('}')
    
    if inicio == -1 or fin == -1 or inicio >= fin:
        return "{}"
    return texto_limpio[inicio : fin + 1]