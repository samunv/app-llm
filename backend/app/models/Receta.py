class Receta:
    def __init__(self, nombrePlato, ingredientes, pasos, especificaciones=""):
        self.nombrePlato = nombrePlato
        self.ingredientes = ingredientes
        self.pasos = pasos
        self.especificaciones = especificaciones
        
    def to_dict(self):
        return {
            "nombrePlato": self.nombrePlato,
            "ingredientes": self.ingredientes,
            "pasos": self.pasos,
            "especificaciones": self.especificaciones or ''
        }