from app.models.Especificaciones import Especificaciones

class SolicitudReceta:

    def __init__(self, comida, modeloIASeleccionado, imagen, tipoImagen, especificaciones: Especificaciones = None):
        self.comida = comida
        self.modeloIASeleccionado = modeloIASeleccionado
        self.imagen = imagen
        self.tipoImagen = tipoImagen
        # Si no se pasa especificaciones, creamos un objeto vacío por defecto
        self.especificaciones = especificaciones or Especificaciones()
