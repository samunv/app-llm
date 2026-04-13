from crewai.tools import BaseTool

class ToolRechazar(BaseTool):
    name: str = "Rechazar_Solicitud"
    description: str = "Úsala cuando la solicitud no sea una receta de cocina válida."

    def _run(self, motivo: str) -> str:
        return "RECHAZADO"