from pydantic import BaseModel
from agents import Agent
from agents import Runner, trace, gen_trace_id
import asyncio  
from dotenv import load_dotenv

load_dotenv(override=True)

class TaskFunctionalityOutput(BaseModel):
    is_asking_about_value_investor: bool
    name: str

def get_classification_agent() -> Agent:
    instructions = ("Check if the user is including any name of value investor and ask for thier perfomance and strategy.")



    classification_agent = Agent( 
        name="Task classifier agent",
        instructions=instructions,
        output_type=TaskFunctionalityOutput,
        model="gpt-4o-mini"
    )
    return classification_agent

if __name__ == "__main__":
    classification_agent = get_classification_agent()
    query = "Tell me about Warren Buffett and his investment strategy."

    with trace("Search over famous value investors"):
        result  = asyncio.run(Runner.run(classification_agent, f"Query: {query}"))

    print("Final output:")   
    print(result.final_output)


