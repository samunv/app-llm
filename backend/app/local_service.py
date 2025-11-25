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
    chat_history: list[BaseMessage] = convertir_historial_a_langchain_messages(datos_solicitud.historial) 

    # Crear la cadena
    chain = prompt_template | llm

    # Definir las entradas (inputs)
    # Se pasa el historial y el nuevo mensaje del usuario
    inputs = {
        "chat_history": chat_history,
        "pregunta_usuario": datos_solicitud.comida
    }
    # La respuesta es un objeto AIMessage
    respuesta_obj = chain.invoke(inputs)

    # Extraer contenido y actualizar historial
    respuesta_ia: str = respuesta_obj.content

    print("LOG>>> RESPUESTA LLM: ", repr(respuesta_ia))
    return extraer_formato_respuesta(respuesta=respuesta_ia)



def convertir_historial_a_langchain_messages(historial: list[dict[str, any]]) -> list[BaseMessage]:
    """
    Convierte el historial a objetos BaseMessage de LangChain (HumanMessage/AIMessage) que el LLM puede procesar.
    """
    messages: list[BaseMessage] = []

    if not historial:
        return messages

    for fila in historial:
        role = fila.get('role')
        parts = fila.get('parts', [])

        content = ""
        if parts and isinstance(parts[0], dict) and 'text' in parts[0]:
            content = parts[0]['text']

        if not content:
            continue

        if role == 'user':
            messages.append(HumanMessage(content=content))
        elif role == 'model':
            messages.append(AIMessage(content=content))

    return messages