from agents import Runner, trace, gen_trace_id
from tracking_over_famouse_value_investors_agent import get_value_investor_agent
from planner_agent import planner_agent, WebSearchItem, WebSearchPlan
from writer_agent import writer_agent, ReportData
from email_agent import email_agent
import asyncio
from agents import Agent
from task_classifier_agent import get_classification_agent
from finance_agents import get_writer_finance_agent

from dotenv import load_dotenv

load_dotenv(override=True)


class ResearchManager:
    def __init__(self):
        self.classifier_agent = get_classification_agent()

        self.investment_agent_1 = get_value_investor_agent(specific_instructions="You should focus on recent market activities and notable investments.")
        self.investment_agent_2 = get_value_investor_agent(specific_instructions="You should emphasize changes in portfolio allocations and investment strategies over the past year.")
        self.investment_agent_3 = get_value_investor_agent(specific_instructions="You should highlight any public statements or writings that shed light on their current investment philosophy.")
        self.writer_finance_agent = get_writer_finance_agent()
    async def run(self, query: str):
        """ Run the deep research process, yielding the status updates and the final report"""
        trace_id = gen_trace_id()

        with trace("Research trace", trace_id=trace_id):
            print(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}")
            yield f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}"
            print("Starting research...")

            is_value_investor_task = await self.check_task(query)

            print("is_value_investor_task:", is_value_investor_task)
            if is_value_investor_task:
                search_results_list = await self.perform_investment_searches(query)
                query_for_writter_agent = "\n\n".join([f"Investment Summary {i+1}:\n{result.final_output}" for i, result in enumerate(search_results_list)])
                query_for_writter_agent = f"Original query: {query}\n\nSummarized investment search results:\n{query_for_writter_agent}"
                yield "Investment searches complete, writing report..."
                report = await Runner.run(
                    self.writer_finance_agent,
                    query_for_writter_agent)
                
                report = report.final_output_as(ReportData)
            else:
                search_plan = await self.plan_searches(query)
                yield "Searches planned, starting to search..."     
                search_results = await self.perform_searches(search_plan)


                yield "Searches complete, writing report..."
                report = await self.write_report(query, search_results)

            yield "Report written, sending email..."
            await self.send_email(report)
            yield "Email sent, research complete"
            yield report.markdown_report
    

    async  def perform_investment_searches(self, query: str) -> list[str]:
        """ Perform searches using specialized investment agents """
        print("Performing investment searches...")
        agents = [self.investment_agent_1, self.investment_agent_2, self.investment_agent_3]
        # Don't call asyncio.run() from inside an already-running event loop.
        # Runner.run(...) returns a coroutine we can schedule directly with create_task.
        num_completed = 0
        tasks = [asyncio.create_task(Runner.run(investor_agent, f"Query: {query}")) for investor_agent in agents]
        results = []
        for task in asyncio.as_completed(tasks):
            try:
                result = await task
                if result is not None:
                    results.append(result)
            except Exception as e:
                # Log the failure and continue with other tasks
                print("Investment search task failed:", e)
            num_completed += 1
            print(f"Searching... {num_completed}/{len(tasks)} completed")
        print("Finished searching")
        return results
    

    async def check_task(self, query: str) -> bool:
        """ Check if the query is asking about value investors """
        print("Classifying task...")
        result = await Runner.run(
            self.classifier_agent,
            f"Query: {query}",
        )
        is_value_investor_task = result.final_output.is_asking_about_value_investor
        print(f"Is value investor task: {is_value_investor_task}")
        return is_value_investor_task
    
    async def plan_searches(self, query: str) -> WebSearchPlan:
        """ Plan the searches to perform for the query """
        print("Planning searches...")
        result = await Runner.run(
            planner_agent,
            f"Query: {query}",
        )
        print(f"Will perform {len(result.final_output.searches)} searches")
        return result.final_output_as(WebSearchPlan)

    async def perform_searches(self, search_plan: WebSearchPlan) -> list[str]:
        """ Perform the searches to perform for the query """
        print("Searching...")
        num_completed = 0
        tasks = [asyncio.create_task(self.search(item)) for item in search_plan.searches]
        results = []
        for task in asyncio.as_completed(tasks):
            result = await task
            if result is not None:
                results.append(result)
            num_completed += 1
            print(f"Searching... {num_completed}/{len(tasks)} completed")
        print("Finished searching")
        return results

    async def search(self, item: WebSearchItem, agent: Agent) -> str | None:
        """ Perform a search for the query """
        input = f"Search term: {item.query}\nReason for searching: {item.reason}"
        try:
            result = await Runner.run(
                agent,
                input,
            )
            return str(result.final_output)
        except Exception:
            return None

    async def write_report(self, query: str, search_results: list[str]) -> ReportData:
        """ Write the report for the query """
        print("Thinking about report...")
        input = f"Original query: {query}\nSummarized search results: {search_results}"
        result = await Runner.run(
            writer_agent,
            input,
        )

        print("Finished writing report")
        return result.final_output_as(ReportData)
    
    async def send_email(self, report: ReportData) -> None:
        print("Writing email...")
        result = await Runner.run(
            email_agent,
            report.markdown_report,
        )
        print("Email sent")
        return report
    

if __name__ == "__main__":
    import asyncio

    r = ResearchManager()

    async def _main():
        # Consume the async generator so the ResearchManager.run coroutine actually executes
        async for update in r.run(query='Tell me about Warren Buffett'):
            print(update)

    asyncio.run(_main())