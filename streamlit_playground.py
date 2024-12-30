import os
import streamlit as st
from dotenv import load_dotenv
from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
import phi

# Load environment variables
load_dotenv()

# Set API key for Phi
phi.api = os.getenv("PHI_API_KEY")
#st.write(f"API Key Loaded: {phi.api}")

# Define the Web Search Agent
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

# Define the Finance Agent
venky_finance_agent = Agent(
    name='Finance Agent',
    role='Provides finance info on stocks',
    model=Groq(id="llama3-groq-70b-8192-tool-use-preview"),
    tools=[
        YFinanceTools(stock_price=True, analyst_recommendations=True, stock_fundamentals=True, company_news=True)        
    ],
    instructions=["Use tables to display the data"],
    add_history_to_messages=True,
    show_tool_calls=True,
    markdown=True,
)

# Show agents' names in the Streamlit app
st.title("AI Agents Playground")
st.write("Here are the available agents:")

st.write(f"- {venky_web_search_agent.name}: {venky_web_search_agent.role}")
st.write(f"- {venky_finance_agent.name}: {venky_finance_agent.role}")

# Interaction Section
st.subheader("Interact with the Agents")

# Web search agent interaction
# Web search agent interaction
web_search_query = st.text_input("Enter a web search query:", "")
if web_search_query:
    st.write(f"Querying web search agent: {web_search_query}")
    try:
        response = venky_web_search_agent.run(messages=[{"role": "user", "content": web_search_query}])
        #st.write(type(response))  # List all attributes and methods of the response object

        #st.write(response)  # Print the entire response to see its structure
        # Assuming the response has an attribute `content`, but this might be different:
        # If response is an object with an attribute `content`, you can try accessing it like this:
        if hasattr(response, 'content'):
            st.write(response.content)  # Access the content attribute
        else:
            st.write("No content available in the response.")
    except Exception as e:
        st.write(f"Error occurred: {str(e)}")

# Finance agent interaction
stock_symbol = st.text_input("Enter a stock symbol:", "")
if stock_symbol:
    st.write(f"Getting data for: {stock_symbol}")
    try:
        response = venky_finance_agent.run(messages=[{"role": "user", "content": stock_symbol}])
        #st.write(response)  # Print the entire response to see its structure
        # Assuming the response has an attribute `content`, but this might be different:
        if hasattr(response, 'content'):
            st.write(response.content)  # Access the content attribute
        else:
            st.write("No content available in the response.")
    except Exception as e:
        st.write(f"Error occurred: {str(e)}")

# Display instructions or additional info
st.write("""
### Instructions:
- **Web Search Agent**: Enter a search query to retrieve information from the web.
- **Finance Agent**: Enter a stock symbol to retrieve financial data for the company.
""")

