from langgraph.graph import StateGraph, START, END
from orchestration.state import AgentState
from orchestration.router import classify_message

from agents.filing_agent import filing_agent
from agents.disaster_event_agent import disaster_event_agent
from agents.weather_agent import weather_agent
from agents.general_agent import general_agent


builder = StateGraph(AgentState)

# Add nodes for each agent and the classifier
builder.add_node("classifier", classify_message)
builder.add_node("filings", filing_agent)
builder.add_node("disaster", disaster_event_agent)
builder.add_node("weather", weather_agent)
builder.add_node("general", general_agent)

builder.add_edge(START, "classifier")

# Add conditional edges based on the classifier's output
builder.add_conditional_edges(
    "classifier",
    lambda state: state["route"],
    {
        "filings": "filings",
        "weather": "weather",
        "disaster": "disaster",
        "general": "general"
    }
)

builder.add_edge("filings", END)
builder.add_edge("disaster", END)   
builder.add_edge("weather", END)
builder.add_edge("general", END)

graph = builder.compile()