import streamlit as st
from src.agent import get_sql_agent
from src.visualizer import visualize_dataframe
import pandas as pd
import json
import os

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="🛒 E-Commerce AI Data Assistant",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------
# SESSION STATE INIT
# ----------------------------
if "history" not in st.session_state:
    st.session_state.history = []  

# ----------------------------
# SIDEBAR (CONVERSATION HISTORY)
# ----------------------------
st.sidebar.title("🗂️ Conversation History")

if st.session_state.history:
    for i, chat in enumerate(reversed(st.session_state.history)):
        with st.sidebar.expander(f" {chat['query'][:30]}..."):
            st.markdown(f"**You:** {chat['query']}")
            st.markdown(f"**AI:** {chat['answer']}")
else:
    st.sidebar.info("No past conversations yet.")

if st.sidebar.button("🧹 Clear History"):
    st.session_state.history = []
    st.sidebar.success("Chat history cleared!")

# ----------------------------
# SIDEBAR SETTINGS
# ----------------------------
st.sidebar.markdown("---")
st.sidebar.header("⚙️ Settings")
show_chart = st.sidebar.checkbox("📈 Show Visualization", value=True)

st.sidebar.markdown("---")
st.sidebar.info(
    "💬 Try asking:\n"
    "- Total revenue by state\n"
    "- Average order value by month\n"
    "- Top 5 customers by sales"
)

# ----------------------------
# MAIN HEADER
# ----------------------------
st.markdown("<h1 style='text-align: center;'>🛒 E-Commerce Data Assistant</h1>", unsafe_allow_html=True)
st.write("<p style='text-align: center; color: grey;'>Ask questions about your e-commerce data and visualize insights instantly.</p>", unsafe_allow_html=True)

# ----------------------------
# DATABASE SETUP
# ----------------------------
DB_PATH = "olist_ecom.db"

if not os.path.exists(DB_PATH):
    st.error("❌ Database not found! Please place 'olist_ecom.db' in the project root folder.")
else:
    # Initialize SQL Agent
    agent = get_sql_agent(DB_PATH)

    # ----------------------------
    # INPUT SECTION
    # ----------------------------
    st.markdown("### 💬 Ask Your Question")
    user_query = st.text_input("Example: 'Top 5 cities with most orders'", placeholder="Type your question here...")

    # ----------------------------
    # PROCESS QUERY
    # ----------------------------
    if st.button("🚀 Run Query", use_container_width=True):
        with st.spinner("🤔 Thinking... Please wait"):
            try:
                structured_query = (
                    user_query
                    + "\nPlease return the answer as JSON with keys 'columns' and 'data', "
                    + "where 'columns' is a list of column names and 'data' is a list of rows."
                )

                response = agent.invoke({"input": structured_query})
                answer = response.get("output", "")

          
                st.success("✅ Query Executed Successfully!")
                with st.expander("🧾 View Full Answer"):
                    st.write(answer)

              
                df = None
                try:
                    json_start = answer.find("{")
                    json_end = answer.rfind("}") + 1
                    json_part = answer[json_start:json_end]
                    result = json.loads(json_part)
                    df = pd.DataFrame(result["data"], columns=result["columns"])
                except Exception:
                    pass

           
                if df is not None and not df.empty:
                    st.markdown("### 📊 Visualization")
                    visualize_dataframe(df, show_chart)
                else:
                    st.info("No structured data detected. Displaying text answer only.")

          
                st.session_state.history.append({"query": user_query, "answer": answer})

            except Exception:
                st.warning("⚠️ That question doesn't seem related to your database.")

# ----------------------------
# FOOTER
# ----------------------------
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color: grey;'>Built with ❤️ using Streamlit, LangChain, and Google Gemini</p>",
    unsafe_allow_html=True
)
