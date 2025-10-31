from agents import Agent, WebSearchTool, ModelSettings


def get_value_investor_agent(specific_instructions:str) -> Agent:
    INSTRUCTIONS = (
    "You are a value investing research assistant. Given a stock ticker or company name, you search the web for financial data, analyst opinions, and market insights related to that company."
    "Produce a concise investment summary of 2–3 paragraphs, under 300 words. Focus on fundamentals — valuation metrics (P/E, P/B, DCF, etc.), business model strength, competitive advantages, management quality, and long-term financial health. Highlight intrinsic value versus current price and any margin of safety. Write succinctly, focusing on substance over style. No filler or speculation. Do not include any commentary beyond the objective investment summary itself."
    ) + ' ' + specific_instructions

    value_investor_agent = Agent(
        name="Search agent",
        instructions=INSTRUCTIONS,
        tools=[WebSearchTool(search_context_size="low")],
        model="gpt-4o-mini",
        model_settings=ModelSettings(tool_choice="required"),
    )

    return value_investor_agent