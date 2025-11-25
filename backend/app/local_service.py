import ollama
from langchain_community.chat_models import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from app.utils import obtener_instrucciones, extraer_formato_respuesta
from app.models import SolicitudReceta

# Inicialización de ChatOllama
llm = ChatOllama(model="gemma:7b", temperature=0.2)

def _obtener_prompt_template(instrucciones: str) -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages(
        [
            # Mensaje del sistema
            ("system", instrucciones),

            # Placeholder para inyectar el historial de chat
            MessagesPlaceholder(variable_name="chat_history"),

            # La pregunta actual del usuario
            ("human", "{pregunta_usuario}"), 
        ]
    )

def generar_respuesta_ia_local(datos_solicitud: SolicitudReceta):
    instrucciones = obtener_instrucciones(datos_solicitud=datos_solicitud)
    prompt_template = _obtener_prompt_template(instrucciones=instrucciones)

    # El historial de chat con tipo List[BaseMessage]
    chat_history: list[BaseMessage] = [] 

    # Crear la cadena
    chain = prompt_template | llm

    # Definir las entradas (inputs)
    # Se pasa el historial y el nuevo mensaje del usuario
    inputs = {
        "chat_history": chat_history,
        "pregunta_usuario": datos_solicitud.comida + ". Si esta pregunta no es sobre comida o solicitando una receta, responde con que tu trabajo es crear recetas."
    }
    # La respuesta es un objeto AIMessage
    respuesta_obj = chain.invoke(inputs)

    # Extraer contenido y actualizar historial
    respuesta_ia: str = respuesta_obj.content

    # Añadir el turno completo (pregunta del usuario + respuesta del modelo) al historial
    chat_history.append(HumanMessage(content=datos_solicitud.comida))
    chat_history.append(AIMessage(content=respuesta_ia))
    
    print("LOG>>> RESPUESTA LLM: ", repr(respuesta_ia))
    return extraer_formato_respuesta(respuesta=respuesta_ia)

def _es_peticion_receta(prompt: str) -> bool:
    """Palabras clave determinar si el usuario pide una receta nueva."""
    prompt_lower = prompt.lower()
    return any(keyword in prompt_lower for keyword in ["receta de", "hazme", "dame la receta", "cocinar", "receta", "haz", "dame", "Prepara", "cocina"])