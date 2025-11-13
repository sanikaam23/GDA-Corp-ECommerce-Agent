
# 🛒 GDA Corp – E-Commerce AI Data Assistant

An AI-powered multi-agent data analysis system built with Streamlit, LangChain, Google GenAI, SQLAlchemy, and LangGraph.
It connects to an E-Commerce database, interprets natural language questions, generates SQL queries, visualizes results, and maintains full conversation history.

## 🚀 Features

### Natural Language → SQL Querying
Convert user questions into SQL automatically using a GenAI-powered SQL agent.

### Real E-Commerce Database
Queries the provided `olist_ecom.db` using SQLAlchemy.

### Data Visualization
Automatically generates charts and tables using Matplotlib, Plotly, and PyDeck.

### Conversation History in Sidebar
Shows the entire session chat flow.

### Multi-Agent Architecture
Uses LangChain + LangGraph to orchestrate:
- SQL Agent
- Visualization Agent
- Insight Agent

### Streamlit Interface
Modern UI with chat experience, visualization toggles, and result preview.

## 📁 Project File Structure

```
GDA-Corp-ECommerce-Agent/
│
├── .venv/                           
│
├── assets/
│   └── architectural diagram.png     
│
├── data/
│   └── olist_ecom.db                
│
├── output/                          
│
├── src/
│   ├── __init__.py
│   ├── agent.py                      
│   ├── database.py                   
│   ├── utils.py                      
│   ├── visualizer.py                 
│   └── prompts/                      
│       └── prompt_templates.txt
│
├── .env                              
├── app.py                            
├── LICENSE
├── README.md
├── requirements.txt
```

## architecture diagram
'''
![Architecture Diagram](assets/architectural diagram.png)

'''

## 🛠️ Setup Instructions

### 1. Clone the repository
```
git clone https://github.com/sanikaam23/GDA-Corp-ECommerce-Agent.git
cd GDA-Corp-ECommerce-Agent
```

### 2. Create and activate a virtual environment
```
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies
```
pip install -r requirements.txt
```

### 4. Add Google API Key
Create a `.env` file:
```
GOOGLE_API_KEY=your_api_key_here
```

### 5. Run the database intially
```
python src/database.py
```

### 6. Run the application
```
streamlit run app.py
```

## 💡 Example Questions

- Top 5 products with highest revenue?
- Show order count by state.
- Which category delivers fastest?
- Monthly sales trend for 2018.
- Most used payment method?

## 🎥 Demo Video Lines (End of Video)

“This Agentic AI system transforms natural language questions into SQL, visualizes insights, and maintains conversation context.
It works like a complete E-Commerce analytics assistant powered by multi-agent reasoning and Google GenAI.”

## 🧠 Tech Stack

| Component | Technology |
|----------|------------|
| UI | Streamlit |
| LLM | Google GenAI (Gemini) |
| Agents | LangChain + LangGraph |
| DB | SQLite (`olist_ecom.db`) |
| Charts | Matplotlib, Plotly, PyDeck |
| Backend | Python 3.11+ |

## 📜 License
MIT License
