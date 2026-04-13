import os
from tavily import TavilyClient
from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class ToolTavilyInput(BaseModel):
    query: str = Field(
        description="Nombre del plato o receta a buscar. Puede ser en español o inglés."
    )


class ToolTavilyBusqueda(BaseTool):
    name: str = "Buscador_Web_Recetas"
    description: str = (
        "Busca recetas en internet cuando no se encuentran en TheMealDB. "
        "Devuelve ingredientes y pasos extraídos de webs de cocina reales. "
        "Úsala como segundo recurso si MealDB no tiene el plato."
    )
    args_schema: type[BaseModel] = ToolTavilyInput

    def _run(self, query: str) -> str:
        client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        
        resultado = client.search(
            query=f"receta {query} ingredientes pasos preparación",
            search_depth="basic",  # "advanced" gasta más créditos
            max_results=3,
            include_answer=True  # ✅ Tavily genera un resumen directo
        )

        if not resultado:
            return "No se encontraron recetas en la web."

        # include_answer genera un resumen directo muy útil para el LLM
        respuesta = []

        if resultado.get("answer"):
            respuesta.append(f"Resumen: {resultado['answer']}")

        for r in resultado.get("results", []):
            respuesta.append(f"Fuente: {r['url']}\n{r['content']}")

        return "\n\n".join(respuesta)