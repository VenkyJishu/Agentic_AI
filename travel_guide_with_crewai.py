
__import__('pysqlite3')
import sys

sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')



import os
from crewai import Agent,Task,Crew,Process, LLM
from crewai_tools import SerperDevTool
from dotenv import load_dotenv
import streamlit as st
import datetime
# import pysqlite3 as sqlite3
import sqlite3
from streamlit import logger

app_logger = logger.get_logger("travel_app")
app_logger.info(f"sqlite version {sqlite3.sqlite_version}")


load_dotenv()

os.environ['GEMINI_API_KEY'] = os.getenv("GEMINI_API_KEY")
os.environ['SERPER_API_KEY'] = os.getenv("SERPER_API_KEY")

# Initialize a search tool (to fetch real-time travel info)
search_tool = SerperDevTool()




# Define the AI Model
llm = LLM(model="gemini/gemini-1.5-flash",
          verbose=True,
          temperature=0.5,
          api_key=os.environ["GEMINI_API_KEY"])

# 🧭 Travel Researcher Agent (Finds historical sites + weather)
researcher_agent = Agent(
    role="Travel Researcher",
    goal="Find historical sites, public transport hotels, and real-time weather for {destination}  from {start_date} to {end_date} .",
    verbose=True,
    memory=True,
    backstory="You are an expert travel researcher, providing up-to-date information about history-focused trips.",
    llm=llm,
    tools=[search_tool],  # Uses live search tool
    allow_delegation=True
)

# 💰 Budget Planner Agent (Ensures trip stays under $1500)
budget_planner_agent = Agent(
    role="Budget Planner",
    goal="Find budget flights, hotels, and activities within {budget} for {destination}  from {start_date} to {end_date} .",
    verbose=True,
    memory=True,
    backstory="You are a skilled budget analyst ensuring trips fit within financial constraints.",
    llm=llm,
    tools=[search_tool],
    allow_delegation=False
)

# 🗺️ Itinerary Planner Agent (Creates a balanced 3-day plan)
itinerary_planner_agent = Agent(
    role="Itinerary Planner",
    goal="Create a  itinerary for {destination}, ensuring all historical sites are covered under {budget}  from {start_date} to {end_date}.",
    verbose=True,
    memory=True,
    backstory="You are an expert in trip planning, ensuring travelers get the best experience within their budget.",
    llm=llm,
    tools=[search_tool],
    allow_delegation=False
)


# Create the research_task  that the agent will perform
research_task = Task(
    name="Research Trip Info",
    description="Find historical sites, public transport hotels, and real-time weather for a given {destination}  from {start_date} to {end_date} .",
    expected_output="A list of top historical sites, a real-time weather update, and 3 hotel options near public transport.",
    tools =[search_tool],
    agent=researcher_agent
)

# 💲 Budget Estimation Task
budget_task = Task(
    name="Budget Estimation",
    description="Find budget flights, hotel options, and daily food/transport costs for {destination}. Ensure total cost stays under {budget}  from {start_date} to {end_date}.",
    expected_output="A full cost breakdown (flights, hotel, food, attractions) ensuring a {budget} budget is maintained.",
    tools=[search_tool],
    agent=budget_planner_agent
)

# 📅 Itinerary Planning Task
itinerary_task = Task(
    name="Itinerary Planning",
    description="Plan a itinerary for {destination}, focusing on historical sites, budget constraints,and real-time weather conditions  from {start_date} to {end_date}.",
    expected_output="A detailed plan, considering weather and budget constraints, with transport recommendations.",
    tools=[search_tool],
    agent=itinerary_planner_agent
)


# 🚀 Crew Setup: All agents working together!
crew = Crew(
    agents=[researcher_agent,budget_planner_agent,itinerary_planner_agent],
    tasks=[research_task,budget_task,itinerary_task],
    process=Process.sequential  # Runs tasks in sequence
)

# Streamlit UI Components
st.title("Travel Guide AI Assistant")

# Input fields for destination and budget
destination = st.text_input("Enter the destination", "London")
budget = st.number_input("Enter your budget (USD)", min_value=100, max_value=10000, value=1500)

# Add date input fields for start and end dates
start_date = st.date_input("Select your trip's start date")
end_date = st.date_input("Select your trip's end date")

# Get today's date
today = datetime.date.today()


# Show an error if the start date is in the past
if start_date and start_date < today:
    st.error("The start date cannot be in the past. Please select a future date.")

# Ensure that the end date is after the start date
if start_date and end_date and end_date < start_date:
    st.error("The end date must be after the start date. Please select a valid end date.")

# Show the steps for the user to interact with the agents
st.subheader("Step 1: Research the Destination")
st.write("We will gather information about historical sites, weather, and hotels nearby.")
# 🔥 Run the CrewAI Trip Advisor system for London with a $1500 budget
#result = crew.kickoff(inputs={'destination': 'London', 'budget': '1500'})
#print(result)




def get_travel_info(destination, budget,start_date,end_date):
    # Here, you would normally call the crew system
    result = crew.kickoff(inputs={'destination': destination, 'budget': str(budget),
                                  'start_date':str(start_date),'end_date':str(end_date)}
                                  )
    st.write(result)
    return result

# Button to start the process
if st.button("Get Travel Info"):
    try:
        if destination and budget:
            with st.spinner('Gathering travel information...'):                      
                      result = get_travel_info(destination, budget, start_date, end_date)
            st.write(result)   # Show the result after the process completes
                  
            if isinstance(result, list):
               for task_output in result:
                  if isinstance(task_output, TaskOutput):
            # You can now safely access the task_output properties like `task_output.name`
                      if task_output.name == 'Research Trip Info':
                          st.subheader("Research Results")
                          st.write(task_output.raw)  # Display the raw result of this task
                      elif task_output.name == 'Budget Estimation':
                          st.subheader("Budget Planning")
                          st.write(task_output.raw)  # Display the raw result of this task
                      elif task_output.name == 'Itinerary Planning':
                          st.subheader("Itinerary")
                          st.write(task_output.raw)  # Display the raw result of this task

    except Exception as e:
        st.error(f"Error occurred: {e}")
