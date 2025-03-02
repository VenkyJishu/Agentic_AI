from phi.agent import Agent
from phi.model.groq import Groq
from dotenv import load_dotenv
from phi.tools.duckduckgo import DuckDuckGo

load_dotenv()

news_agent = Agent(
    name="News Agent",
    model=Groq(id="llama-3.3-70b-versatile"),
    markdown=True,
    tools=[DuckDuckGo()],
    instructions=[
        'Search the latest news about indian stock market',
        'Summarize top 5 topics',
        'Provide key insights in markdown format for read'
    ],
    show_tool_calls=True,
    debug_mode=True

)


stock_agent = Agent(
    name="News Agent",
    model=Groq(id="llama-3.3-70b-versatile"),
    markdown=True,
    tools=[DuckDuckGo()],
    instructions=[
        'Provide which stock will perform needs to be traded today based on current market'
        'Provide key insights in markdown format for read'
    ],
    show_tool_calls=True,
    debug_mode=True

)

multi_ai_agent = Agent(
    team=[news_agent,stock_agent],
    model=Groq(id="llama-3.3-70b-versatile"),
    instructions=["Always include sources","Use tables to display the data"],
    show_tool_calls=True,
    markdown=True,

)


multi_ai_agent.print_response("Summary of the agents",stream=True)