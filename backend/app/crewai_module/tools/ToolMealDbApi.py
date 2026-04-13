import requests
from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class ToolMealDbInput(BaseModel):
    plato: str = Field(
        description="Nombre del plato o receta a buscar en inglés o español."
    )


class ToolMealDbApi(BaseTool):
    name: str = "Buscador_Recetas_MealDB"
    description: str = (
        "Busca recetas detalladas en una base de datos global de cocina internacional. "
        "Úsala cuando el usuario pregunte por recetas que no estén en los videos guardados, "
        "o cuando quiera instrucciones detalladas, ingredientes exactos o recetas de cocina internacional."
    )
    args_schema: type[BaseModel] = ToolMealDbInput

    def _run(self, plato: str) -> str:
        url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={plato}"
        response = requests.get(url)

        if response.status_code != 200:
            return "No se pudo conectar con la base de datos de recetas."

        data = response.json()

        if not data["meals"]:
            return f"No se encontraron recetas para '{plato}'."

        # Tomamos la primera receta
        meal = data["meals"][0]

        # Extraemos ingredientes dinámicamente 
        ingredientes = []
        for i in range(1, 21):
            ingrediente = meal.get(f"strIngredient{i}", "").strip()
            medida = meal.get(f"strMeasure{i}", "").strip()
            # Filtramos solo ingredientes válidos
            if ingrediente:
                ingredientes.append(f"- {medida} {ingrediente}".strip())

        resultado = f"""
 {meal['strMeal']}
Categoría: {meal['strCategory']}
Origen: {meal['strArea']}

 Ingredientes:
{chr(10).join(ingredientes)}

Instrucciones:
{meal['strInstructions'][:1000]}...
"""
        return resultado.strip()