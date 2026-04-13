from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from app.crewai_module.BaseCrew import BaseCrew
from app.crewai_module.tools.ToolTavily import ToolTavilyBusqueda
from app.crewai_module.tools.ToolRechazar import ToolRechazar
from app.models.Receta import Receta


@CrewBase
class CrewJerarquico(BaseCrew):
    agents_config = 'agents/agents.yaml'
    tasks_config = 'agents/tasks.yaml'

    @agent
    def investigador(self) -> Agent:
        return Agent(
        config=self.agents_config['investigador'],
        tools=[ToolTavilyBusqueda(), ToolRechazar()],
        llm=self.llm_rapido,
        allow_delegation=False
    )

    @agent
    def chef(self) -> Agent:
        return Agent(
            config=self.agents_config['chef'],
            llm=self.llm_rapido,
            allow_delegation=False,        )

    @task
    def tarea_investigacion(self) -> Task:
        # Esta tarea se encarga de buscar en ChromaDB (RAG) o usar conocimiento propio
        return Task(
            config=self.tasks_config['tarea_investigacion']
        )

    @task
    def tarea_estructuracion(self) -> Task:
        # Esta tarea toma los datos de la anterior y genera el JSON final
        return Task(
            config=self.tasks_config['tarea_estructuracion'],
            output_json=Receta,
            context=[self.tarea_investigacion()] #Recibe el output de la tarea de investigación para estructurarlo mejor

        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[self.investigador(), self.chef()],
            tasks=[self.tarea_investigacion(), self.tarea_estructuracion()],
            process=Process.hierarchical,
            manager_llm=self.llm,
            verbose=True,
            max_rpm=6 # Máximo 6 ejecuciones por minuto para controlar tokens
        )