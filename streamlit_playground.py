import streamlit as st
from web_finance_agent import web_search_agent,finance_agent



# Show agents' names in the Streamlit app
st.title("Finance and Web AI Agents Playground")
st.write("Here are the available agents:")

st.write(f"- {web_search_agent.name}: {web_search_agent.role}")
st.write(f"- {finance_agent.name}: {finance_agent.role}")

# Interaction Section
st.subheader("Interact with the Agents")

# Display instructions or additional info
st.write("""
### Instructions:
- **Web Search Agent**: Enter a search query to retrieve information from the web.
- **Finance Agent**: Enter a stock symbol to retrieve financial data for the company.
""")

st.title("Web and Finance Agent App")

agent_choice = st.selectbox("Choose an agent:", ["Web Agent", "Finance Agent"])
user_input = st.text_input("Enter your query:")

if st.button("Submit"):
    if agent_choice == "Web Agent":
        response = web_search_agent.get_response(user_input)  # Make sure web_agent is properly set up
    else:
        if user_input:
            # Call finance agent for stock query
            response = finance_agent.run(messages=[{"role": "user", "content": user_input}])
            if 'content' in response:
                st.markdown(response['content'])
            else:
                st.write("No relevant data found for this stock symbol.")
        else:
            st.write("Please enter a valid stock symbol.")



