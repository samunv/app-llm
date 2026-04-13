from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from app.models.RespuestaAgente import RespuestaAgente
from app.crewai_module.BaseCrew import BaseCrew
from app.crewai_module.tools.ToolMemoriaChroma import ToolMemoriaChroma

@CrewBase
class RecetaCrew(BaseCrew):
    """Crew para procesar videos de cocina"""
    agents_config = './agents/agents.yaml'
    tasks_config = './agents/tasks.yaml'

    @agent
    def validador(self) -> Agent:
        return Agent(
            llm=self.llm,
            config=self.agents_config['validador'],
            tools=[ToolMemoriaChroma()], # Agregamos la tool de búsqueda en ChromaDB
            verbose=True
        )

    @agent
    def escritor(self) -> Agent:
        return Agent(
            llm=self.llm, 
            config=self.agents_config['escritor'],
            verbose=True
        )

    @task
    def tarea_clasificacion(self) -> Task:
        return Task(
            config=self.tasks_config['tarea_clasificacion'],
            output_json=RespuestaAgente
        )

    @task
    def tarea_extraccion(self) -> Task:
        return Task(
            config=self.tasks_config['tarea_extraccion'],
            output_json=RespuestaAgente
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents, # Carga automática por los decoradores
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True
        )