from mcp.server.fastmcp import FastMCP
from tools.weather_tool import get_current_weather, get_forecast
from tools.event_search_tool import query_events

mcp = FastMCP("mcp_server")


mcp.tool()(get_current_weather)
mcp.tool()(get_forecast)    
mcp.tool()(query_events)

if __name__ == "__main__":
    mcp.run(transport="stdio")