import os
from dotenv import load_dotenv
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.utilities import SQLDatabase
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()


def get_sql_agent(db_path: str):
    """
    Creates a SQL Agent using ONLY Google Gemini API (no memory buffer).
    """

    db = SQLDatabase.from_uri(f"sqlite:///{db_path}")


    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0,
        convert_system_message_to_human=True
    )

  
    agent = create_sql_agent(
        llm=llm,
        db=db,
        verbose=True
    )

    return agent


if __name__ == "__main__":
    
    DB_PATH = "olist_ecom.db"

    if os.path.exists(DB_PATH):
        agent = get_sql_agent(DB_PATH)
        question = "What is the total revenue by state?"
        try:
            response = agent.invoke({"input": question})
            print("Agent Response:", response["output"])
        except Exception as e:
            print("Error:", e)
    else:
        print("Database not found! Make sure ecommerce.db exists.")