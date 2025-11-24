
import ollama
from langchain_ollama import OllamaLLM
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from app.utils import obtener_instrucciones
from app.models import SolicitudReceta

llm =OllamaLLM(model="llama3.2:1b", temperature=0.1)


def generar_respuesta_ia_local(datos_solicitud: SolicitudReceta):
    #lista incialmente vacia para el historial de chat
    if chat_history is None:
        chat_history = []

    instrucciones = obtener_instrucciones(datos_solicitud=datos_solicitud)
    prompt_template = _obtener_prompt_template(
        instrucciones=instrucciones, 
        prompt_comida=datos_solicitud.comida
    )

    # Formatear el prompt con el historial
    prompt_texto = prompt_template.format_prompt(chat_history=chat_history).to_string()

    # Llamada al LLM
    respuesta_ia = llm(prompt_texto)

    # Actualizar historial
    chat_history.append(HumanMessage(content=datos_solicitud.comida))
    chat_history.append(AIMessage(content=respuesta_ia))

    return respuesta_ia


def _obtener_prompt_template(instrucciones, prompt_comida):
    prompt_template = ChatPromptTemplate.from_messages(
        [
            #mensaje del sistema
            (
                "system",
                instrucciones
            ),
                #placeholder para el historial de chat
                MessagesPlaceholder(variable_name="chat_history"),
                #la pregunta del usuario
                ("human", prompt_comida),
        ]
        
    )

    return prompt_template