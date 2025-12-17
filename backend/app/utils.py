from app.models.SolicitudReceta import SolicitudReceta
from app.models.Especificaciones import Especificaciones
from app.models.Receta import Receta
from app.models.Receta import Ingrediente
import json
import re
from pydantic import ValidationError, BaseModel

JSON_RECETA_OUTPUT = """
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


def obtener_instrucciones_generador_recetas(prompt="", especificaciones:Especificaciones = {}, fuente_info: str = ""):
    prompt = prompt or ""

    return f"""
ROL Y OBJETIVO
Eres ChefGPT, un asistente experto en cocina. Tu función principal es generar recetas y responder preguntas sobre la ÚLTIMA receta que generaste.

FORMATO DE RESPUESTA
1. Si el usuario pide una receta, DEVUELVE SOLO el JSON solicitado. NO añadas texto antes ni después.
2. Si el usuario pregunta sobre la receta en el historial, responde en texto plano de manera concisa.
3. Si el usuario pregunta por algo que no es comida o ingredientes, o no hay receta en el historial, pide amablemente que solicite una receta.
4. Todas tus respuestas deben ser siempre en ESPAÑOL (nunca en otro idioma que no sea Español castellano). Si el usuario trata de pedir las cosas en otro idioma, tú responderás en español.


// ESTRUCTURA JSON (OBLIGATORIA)
OUTPUT ESPERADO PARA LAS RECETAS: {JSON_RECETA_OUTPUT}

CONTEXTO DE LA SOLICITUD
{_prompt_para_receta_con_fuente(fuente_info=fuente_info, especificaciones=especificaciones) if fuente_info else _prompt_para_receta_pedida(prompt_usuario=prompt, especificaciones=especificaciones)}
"""

def _prompt_para_receta_con_fuente(fuente_info: str, especificaciones: Especificaciones)->str:
    return f"""
UTILIZA ESTE TEXTO COMO FUENTE DE INFORMACIÓN PARA REALIZAR LA RECETA: <<{fuente_info}>>
ESPECIFICACIONES DEL USUARIO (Considerálos solamente si son válidas) : << {"Dieta: " + especificaciones.tipo_dieta or "Ninguna" + "; Restricciones: " + especificaciones.restricciones or "Ninguna" + "; Objetivos: " + especificaciones.objetivo or "Ninguno" + "; Añade ingredientes personalizados como: (si los hay) " + especificaciones.ingredientes_disponibles or "Ninguno" } >>
LA RECETA DEBE ESTAR BASADA EN ESE TEXTO COMBINANDO LAS ESPECIFICACIONES DEL USUARIO.
 """



def _prompt_para_receta_pedida(prompt_usuario:str, especificaciones: Especificaciones)->str:

    return f"""
PROMPT O INPUT DEL USUARIO: << {prompt_usuario + ". Dieta: " + especificaciones.tipo_dieta or "Ninguna" + "; Restricciones: " + especificaciones.restricciones  or "Ninguna"+ "; Objetivos: " + especificaciones.objetivo or "Ninguno" + "; Añade ingredientes personalizados como: (si los hay) " + especificaciones.ingredientes_disponibles or "Ninguno"} >> Si el usuario pide algo que no sea sobre comida o preguntas sobre las recetas anteriores, responde EXACTAMENTE:
"Solo puedo ayudarte con recetas de cocina." No generes recetas sobre personas, deportes, política o cualquier otro tema.

"""



def filtrar_palabras_clave(texto: str) -> bool:
    palabras_clave = ["receta", "prepara", "https://www.youtube.com/watch?v=" , "@"]
    texto_lower = texto.lower()
    return any(texto_lower.startswith(palabra) for palabra in palabras_clave)



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

def extraer_video_id(prompt: str) -> str | None:
    if not prompt:
        return None
    patron_regex = r'https://www\.youtube\.com/watch\?v=([\w-]{11}).*' 

    match_url = re.search(patron_regex, prompt)

    if match_url:
        # El grupo de captura 1 sigue conteniendo solo el ID de 11 caracteres
        return match_url.group(1)
    return None