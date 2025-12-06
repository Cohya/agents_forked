from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List


@CrewBase
class Coder2():
    """Coder2 crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    # you should us a docker when you fo it to make sure it want distroy your computer 
    # https://docs.docker.com/desktop/

    @agent 
    def coder(self) -> Agent:
        return Agent(
            config=self.agents_config['coder'],
            verbose=True,
            allow_code_execution=True, # allow the agent to execute code
            code_execution_mode="safe",  # Uses Docker for safety
            max_execution_time=30, # 30 SECONDS TO EXECUTE THE CODE
            max_retry_limit=5 # THISIS THE NUMBER OF TIME IT CAN TRY TO EXECUTE THE CODE
        )

    @task
    def coding_task(self) -> Task:
        return Task(
            config=self.tasks_config['coding_task'],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Coder2 crew"""


        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        
        )
