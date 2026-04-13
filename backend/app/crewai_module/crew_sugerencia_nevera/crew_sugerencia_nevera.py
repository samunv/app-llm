from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from app.models.Receta import Receta
from app.crewai_module.BaseCrew import BaseCrew
from app.crewai_module.tools.ToolBuscadorIngredientes import ToolBuscadorIngredientes


@CrewBase
class SugerenciaNeveraCrew(BaseCrew):
    """Crew secuencial para sugerir recetas a partir de ingredientes disponibles"""
    agents_config = './agents/agents.yaml'
    tasks_config = './agents/tasks.yaml'

    @agent
    def analista_despensa(self) -> Agent:
        return Agent(
            llm=self.llm_rapido,
            config=self.agents_config['analista_despensa'],
            tools=[ToolBuscadorIngredientes()],
            verbose=True
        )

    @agent
    def chef_creativo(self) -> Agent:
        return Agent(
            llm=self.llm,
            config=self.agents_config['chef_creativo'],
            verbose=True
        )

    @task
    def tarea_analisis_despensa(self) -> Task:
        return Task(
            config=self.tasks_config['tarea_analisis_despensa']
        )

    @task
    def tarea_elaboracion_receta(self) -> Task:
        return Task(
            config=self.tasks_config['tarea_elaboracion_receta'],
            output_json=Receta
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
