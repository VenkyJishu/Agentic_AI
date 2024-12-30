from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
from dotenv import load_dotenv
from phi.playground import Playground,serve_playground_app
import phi
import os

load_dotenv()

phi.api = os.getenv("PHI_API_KEY")
print(phi.api)



venky_web_search_agent = Agent(
    name="Web Search Agent",
    role="Search the web for Information",
    model=Groq(id="llama3-groq-70b-8192-tool-use-preview"),
    tools=[DuckDuckGo()],
    instructions=["Always include sources"],
    add_history_to_messages=True,
    show_tool_calls=True,
    markdown=True,
)

venky_finance_agent = Agent(
    name='Finance Agent',
    model=Groq(id="llama3-groq-70b-8192-tool-use-preview"),
    tools=[
        YFinanceTools(stock_price=True,analyst_recommendations=True,stock_fundamentals=True,company_news=True)        
    ],
    instructions=["Use tables to display the data"],
    add_history_to_messages=True,
    show_tool_calls=True,
    markdown=True,
)

# Verify the agents are properly instantiated
print(f"Web Search Agent: {venky_web_search_agent}")
print(f"Finance Agent: {venky_finance_agent}")

app = Playground(agents=[venky_web_search_agent, venky_finance_agent]).get_app()


if __name__ == "__main__":
    print("hitting playground")
    serve_playground_app("playground:app", reload=True)

