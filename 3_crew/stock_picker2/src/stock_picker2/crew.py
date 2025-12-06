from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from pydantic import BaseModel, Field
from crewai_tools import SerperDevTool
from .tools.push_tool import PushNotificationTool
## Memory integration 
from crewai.memory import LongTermMemory, ShortTermMemory, EntityMemory 
from crewai.memory.storage.rag_storage import RAGStorage
from crewai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage
import os
from pathlib import Path 
## Example 
class TrendingCompany(BaseModel):
    """ A company that is in the news and attracting attention """
    name: str = Field(description="Company name")
    ticker: str = Field(description="Stock ticker symbol")
    reason: str = Field(description="Reason this company is trending in the news")

class TrendingCompanyList(BaseModel):
    """ List of multiple trending companies that are in the news """
    companies: List[TrendingCompany] = Field(description="List of companies trending in the news")

class TrendingCompanyResearch(BaseModel):
    """ Research on a trending company """
    name: str = Field(description="Company name")
    market_position: str = Field(description="Current market position and competitive analysis")
    future_outlook: str = Field(description="Future outlook and growth prospects")
    investment_potential: str = Field(description="Investment potential, risks, and sustability for investment")

class TrendingCompanyResearchList(BaseModel):
    """ A list of detailed research on all the companies """
    research_list: List[TrendingCompanyResearch] = Field(description="Comprehensive research on all trending companies")

@CrewBase
class StockPicker2():
    """StockPicker2 crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def trending_company_finder(self) -> Agent:
        """Agent to find trending companies in the news"""
        return Agent(config = self.agents_config['trending_company_finder'],
                     tools = [SerperDevTool()], memory = True)
    
    @agent
    def financial_researcher(self) -> Agent:
        """Agent to research financial details of companies"""
        return Agent(config = self.agents_config['financial_researcher'],
                     tools = [SerperDevTool()])
    
    @agent
    def stock_picker(self)->Agent:
        """Agent to pick stocks based on research"""
        return Agent(config = self.agents_config['stock_picker'],  memory = True) # tools = [PushNotificationTool()] disable it because I do not have license

    @task 
    def find_trending_companies(self) -> Task:
        """Task to find trending companies in the news"""
        return Task(config = self.tasks_config['find_trending_companies'],
                    input_model = None,
                    output_pydantic= TrendingCompanyList) # by defining the output_podyantic, CrewAI can validate the output structure
    
    @task 
    def research_trending_companies(self) -> Task:
        """Task to research trending companies"""
        return Task(config = self.tasks_config['research_trending_companies'],
                    output_pydantic= TrendingCompanyResearchList)
    
    @task
    def pick_best_company(self) -> Task:
        """Task to pick the best company to invest in"""
        return Task(config = self.tasks_config['pick_best_company'])  
    
    @crew
    def crew(self) -> Crew:
        """Define the StockPicker2 crew with its agents and tasks"""

        # Get the project root directory (where memory folder is located)
        # crew.py is at: stock_picker2/src/stock_picker2/crew.py
        # project root is at: stock_picker2/
        project_root = Path(__file__).parent.parent.parent
        # memory_dir = project_root / "memory"
        # memory_dir.mkdir(exist_ok=True)
        memory_dir = project_root / "memory"

        if memory_dir.exists():
    # delete old content (careful)
            for p in memory_dir.iterdir():
                if p.is_file(): p.unlink()
                else: import shutil; shutil.rmtree(p)


        os.environ["CREWAI_STORAGE_DIR"] = str(memory_dir.absolute())

        if "OPENAI_API_KEY" in os.environ:
            os.environ.setdefault("CHROMA_OPENAI_API_KEY", os.environ["OPENAI_API_KEY"])
        

        manager = Agent(config=self.agents_config['manager'],
                        allow_delegation=True) # Telling crew that we can delegate tasks to other agents
        
        # short_term_memory = ShortTermMemory(
        #                 storage = RAGStorage(
        #                         embedder_config={
        #                             "provider": "openai",
        #                             "config": {
        #                                 "model_name": 'text-embedding-3-small'
        #                             }
        #                         },
        #                         type="short_term",
        #                         path=str(memory_dir.absolute())
        #                     )
        #                 )

        # long_term_memory = LongTermMemory(
        #     storage=LTMSQLiteStorage(
        #         db_path=str(memory_dir / "long_term_memory_storage.db")
        #     )
        # )

        # entity_memory = EntityMemory(
        #                 storage=RAGStorage(
        #                     embedder_config={
        #                         "provider": "openai",
        #                         "config": {
        #                             "model_name": 'text-embedding-3-small'
        #                         }
        #                     },
        #                     type="short_term",
        #                     path=str(memory_dir.absolute())
        #                 )
        #             )

        return Crew(agents = self.agents,
                    tasks = self.tasks,
                    process=Process.hierarchical,
                    verbose=True,
                    manager_agent=manager, 
                    # long_term_memory=long_term_memory,
                    # short_term_memory=short_term_memory,
                    memory = False, # if this is false the agents cannot use memory, memory in window is problematic and ebenmore in uv env 
                    # entity_memory=entity_memory
            #               embedder={
            # "provider": "openai",
            # "config": {"model": "text-embedding-3-small"}
            #             }
        )
