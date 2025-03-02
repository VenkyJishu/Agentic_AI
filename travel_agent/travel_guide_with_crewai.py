import os
from crewai import Agent,Task,Crew,Process, LLM
from crewai_tools import SerperDevTool
from dotenv import load_dotenv
import streamlit as st 
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
    goal="Find historical sites, public transport hotels, and real-time weather for {destination}.",
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
    goal="Find budget flights, hotels, and activities within {budget} for {destination}.",
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
    goal="Create a 3-day itinerary for {destination}, ensuring all historical sites are covered under {budget}.",
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
    description="Find historical sites, public transport hotels, and real-time weather for a given {destination} .",
    expected_output="A list of top historical sites, a real-time weather update, and 3 hotel options near public transport.",
    tools =[search_tool],
    agent=researcher_agent
)

# 💲 Budget Estimation Task
budget_task = Task(
    description="Find budget flights, hotel options, and daily food/transport costs for {destination}. Ensure total cost stays under {budget}.",
    expected_output="A full cost breakdown (flights, hotel, food, attractions) ensuring a $1500 budget is maintained.",
    tools=[search_tool],
    agent=budget_planner_agent
)

# 📅 Itinerary Planning Task
itinerary_task = Task(
    description="Plan a 3-day itinerary for {destination}, focusing on historical sites, budget constraints, and real-time weather conditions.",
    expected_output="A detailed 3-day plan, considering weather and budget constraints, with transport recommendations.",
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


# Show the steps for the user to interact with the agents
st.subheader("Step 1: Research the Destination")
st.write("We will gather information about historical sites, weather, and hotels nearby.")
# 🔥 Run the CrewAI Trip Advisor system for London with a $1500 budget
#result = crew.kickoff(inputs={'destination': 'London', 'budget': '1500'})
#print(result)



@st.cache_data
def get_travel_info(destination, budget):
    # Here, you would normally call the crew system
    result = crew.kickoff(inputs={'destination': destination, 'budget': str(budget)})
    return result

# Button to start the process
if st.button("Get Travel Info"):
    if destination and budget:
        # Run the CrewAI system
        result = get_travel_info(destination, budget)
        st.write(result)
        
            # Assuming the structure of result is different, you'll need to adjust how you access it
        # If the structure is different, you'll need to use the correct key
        # If tasks are stored in a list or dictionary with task names as keys
        if isinstance(result, dict):
    # Check if the task results are in a list of tasks
            if 'tasks' in result:
                for task in result['tasks']:
                    if task['name'] == 'Research Trip Info':
                        st.subheader("Research Results")
                        st.write(task['result'])
                    elif task['name'] == 'Budget Estimation':
                        st.subheader("Budget Planning")
                        st.write(task['result'])
                    elif task['name'] == 'Itinerary Planning':
                        st.subheader("Itinerary")
                        st.write(task['result'])

    else:
        st.error("Please enter both a valid destination and a budget.")