from writer_agent import ReportData
from  agents import Agent


def get_writer_finance_agent() -> Agent:
    instructions = (
        "You are a senior financial researcher tasked with writing a cohesive report for a financial research query. "
        "You will be provided with the original query, and some initial research done by a research assistant.\n"
        "You should first come up with an outline for the report that describes the structure and "
        "flow of the report. Then, generate the report and return that as your final output.\n"
    )

    writer_finance_agent = Agent(
        name="Writer Finance Agent",
        instructions=instructions,
        model="gpt-4o-mini",
        output_type=ReportData,
    )

    return writer_finance_agent