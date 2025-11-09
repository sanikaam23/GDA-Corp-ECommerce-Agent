# ================================
# GDA-Corp E-Commerce Data Analyst Agent
# app.py
# ================================

import sys
import os
import streamlit as st
from dotenv import load_dotenv, find_dotenv

# --- Path Setup (ensures src/ is importable) ---
# Assuming 'src' is a subdirectory at the same level as 'app.py'
# In this structure, the path setup is already correct for the provided code context.
sys.path.append(os.path.join(os.getcwd(), "src"))

# Import from src/agent.py and src/database.py
from src.agent import get_sql_agent
from src.database import load_data_to_db # This import assumes 'src/database.py' exists

# --- Streamlit Configuration ---
st.set_page_config(page_title="GDA-Corp E-Commerce Agent", layout="wide")

# --- Environment Setup ---
st.write("✅ Streamlit initialized")
load_dotenv(find_dotenv())
st.write("✅ .env loaded:", bool(os.getenv("GOOGLE_API_KEY")))

# --- Constants ---
DB_NAME = "olist_ecom.db"

# --- Setup Function ---
@st.cache_resource
def setup_database_and_agent():
    """Loads the database and initializes the LangChain + Gemini SQL agent."""
    st.write("🔧 Starting database and agent setup...")
    try:
        # 1️⃣ Build database if missing
        if not os.path.exists(DB_NAME):
            st.warning("Database not found. Attempting to build from data/ directory...")
            # Assuming load_data_to_db() handles the creation and returns the path
            db_path = load_data_to_db() 
        else:
            db_path = os.path.join(os.getcwd(), DB_NAME)
        st.write("📂 Database path:", db_path)

        # 2️⃣ Initialize the agent
        agent = get_sql_agent(db_path)
        if agent:
            st.success("🤖 Agent initialized successfully!")
        else:
            st.error("❌ Failed to initialize the agent.")
        return agent

    except Exception as e:
        st.error(f"Database/Agent Setup Failed: {e}")
        return None


# --- Main Streamlit Interface ---
st.title("🛒 E-Commerce Data Analyst Agent")
st.caption("Powered by Gemini and LangChain for Text-to-SQL Insights")

# --- Sidebar ---
with st.sidebar:
    st.header("⚙️ Setup & Architecture")

    if os.path.exists(DB_NAME):
        st.success(f"Database '**{DB_NAME}**' loaded.")
    else:
        st.error(f"Database '**{DB_NAME}**' not found. Please run `python src/database.py` first.")

    st.markdown("---")
    st.subheader("System Architecture")
    st.markdown(
        """
- **LLM**: **Gemini-2.5-Flash** (via LangChain)
- **Framework**: **LangChain Agent**
- **Data**: **SQLite** (Text-to-SQL)
- **UI**: **Streamlit**
        """
    )

    st.markdown("---")
    st.subheader("Creative Features")
    st.markdown(
        """
- 🧠 **Memory**: Contextual follow-ups (via LangChain memory)
- 📊 **Visualization**: Future chart integration (`src/utils.py`)
- 🌍 **Translation**: Handles Portuguese product names
        """
    )

# --- Agent Initialization ---
agent_executor = setup_database_and_agent()

# --- Chat Interface ---
if agent_executor:
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "Hello! 👋 I am your E-Commerce Data Analyst Agent. "
                    "You can ask me about sales, categories, reviews, or delivery performance."
                ),
            }
        ]

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Handle new user input
    if prompt := st.chat_input("Ask a question about the Olist dataset..."):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # Ensure the Streamlit container is here for the spinner and output
            with st.spinner("Analyzing data and generating SQL query..."):
                try:
                    # Invoke the agent executor
                    response = agent_executor.invoke({"input": prompt})

                    # Debug: show raw Gemini response
                    # st.write("🔍 Raw agent response:", response) # Keeping for debug visibility

                    # --- Safe response handling ---
                    if response is None:
                        agent_output = "⚠️ No response from agent. Try rephrasing your question."
                    elif isinstance(response, dict):
                        # Extract final output
                        agent_output = response.get("output", "⚠️ No 'output' key found in response.")
                    elif isinstance(response, str):
                        agent_output = response
                    else:
                        agent_output = f"⚠️ Unexpected response type: {type(response)}"

                    # --- Show generated SQL query if available ---
                    # The LangChain agent returns the SQL query in the intermediate_steps
                    if isinstance(response, dict) and "intermediate_steps" in response:
                        st.markdown("🧩 **Generated SQL Query (Intermediate Steps):**")
                        # Look through the intermediate steps for the tool call input (the SQL query)
                        for step in response["intermediate_steps"]:
                            # The 'step' is a tuple (AgentAction, Observation)
                            # AgentAction has 'tool', 'tool_input', 'log'
                            # We can print the action's tool_input (which is the query)
                            if len(step) > 0 and hasattr(step[0], 'tool_input'):
                                # Check if the tool is the one executing the SQL
                                if 'sql_db_query' in step[0].tool:
                                    st.code(str(step[0].tool_input), language="sql")

                    # --- Display final output ---
                    st.markdown(agent_output)

                except Exception as e:
                    st.error(f"An error occurred during agent execution: {e}")
                    agent_output = f"Sorry, I encountered a technical error: {str(e)}"

            # Add final output to chat history
            st.session_state.messages.append({"role": "assistant", "content": agent_output})
else:
    st.error("❌ **Agent initialization failed.** Check your `.env` file (for `GOOGLE_API_KEY`) and database setup.")