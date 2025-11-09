import streamlit as st
from src.agent import get_sql_agent
import os

st.set_page_config(page_title="E-Commerce AI SQL Assistant")

st.title("🛒 E-Commerce Data Assistant (Google Gemini)")
st.write("Ask any question about your database in natural language.")

# Path to SQLite Database
DB_PATH = "olist_ecom.db"

if not os.path.exists(DB_PATH):
    st.error("❌ Database not found! Please create 'ecommerce.db' in the data folder.")
else:
    # Initialize SQL Agent
    agent = get_sql_agent(DB_PATH)

    user_query = st.text_input("💬 Ask a question like 'Top 5 cities with most orders'")

    if st.button("Submit") and user_query:
        with st.spinner("Processing..."):
            try:
                response = agent.invoke({"input": user_query})
                st.success("✅ Success!")
                st.subheader("📊 Result:")
                st.write(response["output"])
            except Exception as e:
                st.error(f"❌ Error: {e}")
