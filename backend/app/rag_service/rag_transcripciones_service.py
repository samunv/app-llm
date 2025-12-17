# Lo primero que se debe hacer es llamar al cliente de ChromaDB
from app.models.Receta import Receta
from app.models.VideoInfo import VideoInfo
from app.config.chromadb_client import coleccion_transcripciones_de_yt

def obtener_receta_semantica_de_transcripciones(video_info:VideoInfo, transcripcion:str = "")->str:
    # verificar la existencia de documentos de X video_id (estará en la metadata).
    # Si no existe, insertar las transcripciones en la base de datos
    if not _verificar_transcripcion_registrada(video_info.video_id):
        _insertar_transcripcion(video_info=video_info ,transcripcion=transcripcion)

    # Obtener ingredientes y pasos
    nombre_receta = video_info.titulo
    fragmentos_ingredientes = _obtener_fragmentos_ingredientes(video_id=video_info.video_id)
    fragmentos_pasos = _obtener_fragmentos_pasos(video_id=video_info.video_id)

    fragmentos_ingredientes_unicos = list(set(fragmentos_ingredientes))
    fragmentos_pasos_unicos =list(set(fragmentos_pasos))

    texto_ingredientes = "; ".join(fragmentos_ingredientes_unicos)
    texto_pasos = "; ".join(fragmentos_pasos_unicos)

    RECETA_SEMANTICA = f"""
    Nombre de la receta: {nombre_receta}
    Información disponible de los ingredientes: << {texto_ingredientes} >>
    Información disponible sobre los pasos principales: << {texto_pasos} >>
    """

    return RECETA_SEMANTICA

def _verificar_transcripcion_registrada(video_id:str)->bool:
    resultado = coleccion_transcripciones_de_yt.get(
        ids=[f"{video_id}_0"], # Verificamos al menos el primer fragmento
        include=[] 
    )
    return len(resultado['ids']) > 0


def _insertar_transcripcion(video_info: VideoInfo, transcripcion: str):
    # tamaño (aprox 200-250 tokens)
    CHUNKS = 1000

    # Dividir el texto en fragmentos
    fragmentos = []
    for i in range(0, len(transcripcion), CHUNKS):
        fragmentos.append(transcripcion[i : i + CHUNKS])

    # Crear IDs únicos para cada fragmento con video_id + posicion
    ids_fragmentos = [f"{video_info.video_id}_{i}" for i in range(len(fragmentos))]

    # Crear metadatos
    metadatos = [{"video_id": video_info.video_id, "titulo": video_info.titulo} for _ in fragmentos]

    coleccion_transcripciones_de_yt.upsert(
        documents=fragmentos,
        ids=ids_fragmentos,
        metadatas=metadatos
    )

    print(f"Se han insertado {len(fragmentos)} fragmentos para el video {video_info.video_id}")


def _obtener_fragmentos_ingredientes(video_id: str) -> list:
    resultados = coleccion_transcripciones_de_yt.query(
        query_texts=[
    "¿Qué ingredientes, alimentos y cantidades se utilizan?",
    "Lista de la compra para la receta",
    "Lo que vamos a necesitar para cocinar"
], 
        n_results=3,
        where={"video_id": video_id},
        include=["documents", "distances"]
    )

    # Verificar si hay resultados
    if not resultados or not resultados['documents'][0]:
        return []

    return _obtener_fragmentos_cercanos(resultados)

def _obtener_fragmentos_pasos(video_id:str)->list:
    resultados = coleccion_transcripciones_de_yt.query(
        query_pasos = [
    "Instrucciones de cocina paso a paso",
    "Preparación, cocinado, tiempos y temperaturas",
    "Primero hacemos esto, después añadimos aquello",
    "Cómo preparar y finalizar el plato"
        ],
        n_results=5,
        where={"video_id": video_id},
        include=["documents", "distances"]
    )

    # Verificar si hay resultados
    if not resultados or not resultados['documents'][0]:
        return []

    return _obtener_fragmentos_cercanos(resultados)

def _obtener_fragmentos_cercanos(resultados: dict):
    # Filtrar: Solo nos quedamos con los docs cuya distancia sea menor a 1.0
    fragmentos_cercanos = []
    for doc, dist in zip(resultados['documents'][0], resultados['distances'][0]):
        if dist < 1.0:
            fragmentos_cercanos.append(doc)
    return fragmentos_cercanos