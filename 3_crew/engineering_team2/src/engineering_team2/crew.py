from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class EngineeringTeam2():
    """EngineeringTeam2 crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def engineering_lead(self) -> Agent:
        return Agent(
            config=self.agents_config['engineering_lead'],
            verbose=True
        )
    
    @agent
    def backend_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['backend_engineer'],
            verbose=True,
            allow_code_execution=True,
            code_execution_mode="safe",
            max_execution_time=240,  # 4 minutes
            max_retries=5,
        )
    
    @agent
    def frontend_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['frontend_engineer'],
            verbose=True,
        )
    
    @agent
    def test_engineer(self) -> Agent:  
        return Agent(
            config=self.agents_config['test_engineer'],
            verbose=True,
            allow_code_execution=True,
            code_execution_mode="safe",
            max_execution_time=240,  # 4 minutes
            max_retries=5,
        )
    
    @agent
    def secretary_note_taker(self) -> Agent:
        return Agent(
            config=self.agents_config['secretary_note_taker'],
            verbose=True,
        )


    @task
    def design_task(self) -> Task:
        return Task(
            config=self.tasks_config['design_task'],
        )
    
    @task
    def code_task(self) -> Task:
        return Task(
            config=self.tasks_config['code_task'],
        )
    
    @task
    def frontend_task(self) -> Task:
        return Task(
            config=self.tasks_config['frontend_task'],
        )
    
    @task
    def test_task(self) -> Task:
        return Task(
            config=self.tasks_config['test_task'],
        )
    
    @task 
    def note_taking_task(self) -> Task:
        return Task(config = self.tasks_config['note_taking_task'])

    @task
    def refined_note_taking_task(self) -> Task:
        return Task(config = self.tasks_config['refined_note_taking_task'])

    @task
    def executer_task(self) -> Task:
        return Task(config = self.tasks_config['executer_task'])

    @crew
    def crew(self) -> Crew:
        """Creates the EngineeringTeam2 crew"""

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )