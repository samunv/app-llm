from app.models.Especificaciones import Especificaciones

class SolicitudReceta:

    def __init__(self, prompt="", modeloIASeleccionado="", imagen="", tipoImagen="", especificaciones: Especificaciones = None, historial=None):
        self.prompt = prompt
        self.modeloIASeleccionado = modeloIASeleccionado
        self.imagen = imagen
        self.tipoImagen = tipoImagen
        self.especificaciones = especificaciones or Especificaciones()
        # Historial será una lista de diccionarios: [{'role': 'user', 'parts': '...'}, ...]
        self.historial = historial or []