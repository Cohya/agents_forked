
from agents import Agent, WebSearchTool, ModelSettings
from agents import Runner, trace, gen_trace_id
# from IPython.display import display, Markdown
import asyncio
from dotenv import load_dotenv
from rich.markdown import Markdown
from rich.console import Console


load_dotenv(override=True)

def get_value_investor_agent(specific_instructions :str = '') -> Agent:
    INSTRUCTIONS = (
        "You are a value investing research assistant. You will be provided with the name of a value investor or a list of names. "
        "Search the web for each investor and produce a concise investment summary of 2–5 paragraphs (under 300 words). "
        "Focus on their recent investments, positions, divestments, and any public statements or writings that shed light on their current investment philosophy. "
        "Highlight intrinsic value versus current price and any margin of safety. "
        "Provide a clear list of the main stocks or assets they are currently invested in, including the percentage of their portfolio each holding represents. "
        "For each holding, show how the percentage changed over the past year, in the format: 'Company X 30% → 24% (sold)' or 'Company Y 15% → 20% (added)'. "
        "Write succinctly, focusing on substance over style. No filler, speculation, or commentary beyond the objective investment summary. "
        "If the name is not a recognized value investor, respond with: 'No relevant information found on this name as a value investor.'"
    )+ ' ' + specific_instructions

   

    value_investor_agent = Agent(
        name="Search agent",
        instructions=INSTRUCTIONS,
        tools=[WebSearchTool(search_context_size="low")],
        model="gpt-4o-mini",
        model_settings=ModelSettings(tool_choice="required"),
    )
    return value_investor_agent


if  __name__ == "__main__":
    value_investor_agent = get_value_investor_agent()
    names_of_value_investors = ["Warren Buffett", "Seth Klarman", "Howard Marks", "Michael Burry"]
    query = ", ".join(names_of_value_investors)
    print(query)
    
    with trace("Search over famous value investors"):
        result  = asyncio.run(Runner.run(value_investor_agent, f"Query: {query}"))

    print("Final output:")   
    console = Console()
    console.print(Markdown(result.final_output))

