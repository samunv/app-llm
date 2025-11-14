class Especificaciones:
    def __init__(self, tipo_dieta, restricciones, ingredientes_evitar, tiempo_maximo, objetivo):
        tipo_dieta
        restricciones
        ingredientes_evitar
        tiempo_maximo
        objetivo

class SolicitudReceta:

    def __init__(self, comida, especificaciones: Especificaciones, modeloIASeleccionado):
        self.comida = comida
        self.especificaciones = especificaciones
        self.modeloIASeleccionado = modeloIASeleccionado

