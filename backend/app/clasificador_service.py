
# Servicio para clasificar si la transcripción es una receta o no
def clasificar_video(titulo_video:str, transcripcion:str = "")->bool:

    # Filtrar primero si el titulo tiene la palabra receta
    if _es_receta_por_titulo(titulo=titulo_video):
        return True
    
    if es_receta(transcripcion=transcripcion):
        return True

    return False

def es_receta(transcripcion: str) -> bool:
    genericas = ["receta", "preparar", "ingredientes", "cocinar", "cocina",
                 "pasos", "procedimiento", "instrucciones", "plato", "comida",
                 "platillo", "preparación"]
    acciones = ["freír", "asar", "hornear", "batir", "mezclar", "revolver",
                "cocer", "hervir", "saltear", "marinar"]
    ingredientes_comunes = ["pollo", "carne", "pescado", "huevo", "arroz",
                            "aceite", "sal", "pimienta", "tomate", "cebolla",
                            "ajo", "azúcar", "mantequilla"]

    texto = transcripcion.lower()
    n_genericas = sum(1 for g in genericas if g in texto)
    n_acciones = sum(1 for a in acciones if a in texto)
    n_ingredientes = sum(1 for i in ingredientes_comunes if i in texto)

    n_palabras_totales = _contar_palabras(transcripcion)

    # Ajustar el rango según la cantidad de palabras
    if n_palabras_totales < 400:  # vídeo muy corto
        return n_acciones >= 1 and n_ingredientes >= 1 and n_genericas >= 1
    elif n_palabras_totales < 1000:  # vídeo corto
        return n_acciones >= 1 and n_ingredientes >= 1 and n_genericas >= 2
    else:  # vídeo largo
        return n_acciones >= 2 and n_ingredientes >= 2 and n_genericas >= 3


def _contar_palabras(texto: str) -> int:
    return len(texto.split())


def _es_receta_por_titulo(titulo: str) -> bool:
    titulo = titulo.lower()
    return "receta" in titulo