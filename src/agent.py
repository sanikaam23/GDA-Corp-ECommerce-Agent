# ================================
# GDA-Corp E-Commerce Data Analyst Agent
# src/agent.py
# ================================

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.utilities import SQLDatabase
from langchain.memory import ConversationBufferMemory
from langchain.agents import AgentExecutor
from typing import Optional

# Load environment variables (ensure this is run in any context where the agent is used standalone)
load_dotenv()


def get_sql_agent(db_path: str) -> Optional[AgentExecutor]:
    """
    Initializes and returns the LangChain Text-to-SQL Agent powered by Gemini.

    Args:
        db_path: Path to the SQLite database (e.g., 'olist_ecom.db').

    Returns:
        AgentExecutor instance ready to handle queries, or None on failure.
    """
    try:
        # --- 1️⃣ Load Gemini / Google API Key ---
        gemini_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        if not gemini_key:
            raise ValueError("GOOGLE_API_KEY not found. Please set it in your .env file.")

        # --- 2️⃣ Initialize Gemini LLM ---
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=gemini_key,
            temperature=0.1
        )

        # --- 3️⃣ Connect to SQLite Database ---
        if not os.path.exists(db_path):
            print(f"❌ Database file not found at {db_path}. Run src/database.py first.")
            return None

        # LangChain utility to connect to a SQL database
        db = SQLDatabase.from_uri(f"sqlite:///{db_path}")

        # --- 4️⃣ Load Custom Prompt Template ---
        # The prefix argument takes a string that is prepended to the standard agent prompt
        prompt_file = "src/prompts/sql_agent_prompt.txt"
        if os.path.exists(prompt_file):
            with open(prompt_file, "r", encoding="utf-8") as f:
                custom_prompt_template = f.read()
        else:
            print(f"⚠️ Custom prompt not found at {prompt_file}. Using default prompt.")
            custom_prompt_template = (
                "You are an expert data analyst. Generate accurate SQL queries "
                "for the given question and return clear, concise answers. "
                "Focus on the Olist e-commerce dataset."
            )

        # --- 5️⃣ Enable Conversation Memory ---
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

        # --- 6️⃣ Create SQL Agent ---
        agent_executor = create_sql_agent(
            llm=llm,
            db=db,
            # 'openai-tools' is a good agent type for Gemini for reliable tool use
            agent_type="openai-tools", 
            verbose=True, # For debugging and seeing intermediate steps in console
            agent_executor_kwargs={
                "memory": memory,
                "handle_parsing_errors": True
            },
            prefix=custom_prompt_template # Pass the custom system instruction here
        )

        # ✅ 7️⃣ Force LangChain to always return structured responses
        # Ensures that 'output' and 'intermediate_steps' are in the response dictionary
        # This is a crucial step for Streamlit's robust response handling.
        agent_executor.return_intermediate_steps = True
        agent_executor.handle_parsing_errors = True
        agent_executor.verbose = True # Redundant with the previous 'verbose=True' but good for clarity

        print("✅ SQL Agent initialized successfully.")
        return agent_executor

    except Exception as e:
        print(f"❌ Failed to initialize SQL Agent: {e}")
        return None


# --- Standalone Test Block ---
if __name__ == '__main__':
    # Adjust this path if running from a different directory
    DB_FILE = os.path.join(os.getcwd(), "olist_ecom.db") 
    print(f"Attempting to initialize agent using {DB_FILE}...")

    if os.path.exists(DB_FILE):
        agent = get_sql_agent(DB_FILE)
        if agent:
            query = "What is the average review score by product category?"
            print(f"\nUser Query: {query}")
            try:
                # Invoke the agent
                response = agent.invoke({"input": query}) 
                print("\n🧩 Raw Agent Response:", response)
                
                # Extract and print final output
                if isinstance(response, dict):
                    print("\n✅ Agent Output:", response.get("output", "No output field found."))
                    
                    # Print the generated SQL query for inspection
                    if "intermediate_steps" in response:
                        print("\nGenerated SQL Queries:")
                        for step in response["intermediate_steps"]:
                            # Check if the step is an action that involves executing a query
                            if len(step) > 0 and hasattr(step[0], 'tool_input') and 'sql_db_query' in step[0].tool:
                                print(f"-> {step[0].tool_input}")

                else:
                    print("\n⚠️ Unexpected response type:", type(response))
            except Exception as e:
                print(f"⚠️ Agent Invocation Error: {e}")
        else:
            print("❌ Agent initialization failed.")
    else:
        print(f"❌ Database not found at {DB_FILE}. Please run 'python src/database.py' first.")