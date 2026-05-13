from mcp_client.client import MCPClient
from mcp_client.async_runner import runner
import json

client = MCPClient()


def initialize_mcp():
    runner.run(client.connect())


def call_tool_sync(tool_name, arguments):
    return runner.run(
        client.call_tool(tool_name, arguments)
    )


def get_tools():
    return client.tools

def get_tools_format() -> dict:
    tools = []

    for tool in client.tools:
        parameters = tool.inputSchema or {}

        if "type" not in parameters:
            parameters = {"type": "object", "properties": parameters}

        tools.append({
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description or "",
                "parameters": parameters,
            }
        })
    return tools
    

def handle_tool_call(message):
    tool_call = message.tool_calls[0]

    tool_name = tool_call.function.name
    arguments = json.loads(tool_call.function.arguments)

    tool_result = call_tool_sync(tool_name, arguments)

    response = {
            "role": "tool",
            "content": str(tool_result),
            "tool_call_id": tool_call.id
    }

    return response