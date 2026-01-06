from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from mypress_agency.tools.custom_tools import rag_retriever_tool, wp_publisher_tool, image_generator_tool

@CrewBase
class MyPressAgencyCrew():
    """MyPressAgency crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def content_strategist(self) -> Agent:
        return Agent(
            config=self.agents_config['content_strategist'],
            tools=[rag_retriever_tool],
            verbose=True
        )

    @agent
    def seo_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['seo_specialist'],
            verbose=True
        )

    @agent
    def copywriter(self) -> Agent:
        return Agent(
            config=self.agents_config['copywriter'],
            verbose=True
        )

    @agent
    def content_editor(self) -> Agent:
        return Agent(
            config=self.agents_config['content_editor'],
            verbose=True
        )

    @agent
    def proofreader(self) -> Agent:
        return Agent(
            config=self.agents_config['proofreader'],
            verbose=True
        )

    @agent
    def designer(self) -> Agent:
        return Agent(
            config=self.agents_config['designer'],
            tools=[image_generator_tool],
            verbose=True
        )

    @agent
    def social_media_manager(self) -> Agent:
        return Agent(
            config=self.agents_config['social_media_manager'],
            verbose=True
        )

    @agent
    def publisher(self) -> Agent:
        return Agent(
            config=self.agents_config['publisher'],
            tools=[wp_publisher_tool],
            verbose=True
        )

    @task
    def strategy_task(self) -> Task:
        return Task(
            config=self.tasks_config['strategy_task'],
        )

    @task
    def seo_task(self) -> Task:
        return Task(
            config=self.tasks_config['seo_task'],
        )

    @task
    def writing_task(self) -> Task:
        return Task(
            config=self.tasks_config['writing_task'],
        )

    @task
    def editing_task(self) -> Task:
        return Task(
            config=self.tasks_config['editing_task'],
        )

    @task
    def proofreading_task(self) -> Task:
        return Task(
            config=self.tasks_config['proofreading_task'],
        )

    @task
    def design_task(self) -> Task:
        return Task(
            config=self.tasks_config['design_task'],
        )

    @task
    def social_media_task(self) -> Task:
        return Task(
            config=self.tasks_config['social_media_task'],
        )

    @task
    def publishing_task(self) -> Task:
        return Task(
            config=self.tasks_config['publishing_task'],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the MyPressAgency crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
