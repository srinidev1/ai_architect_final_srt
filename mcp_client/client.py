from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters


class MCPClient:
    def __init__(self):
        self.server_params = StdioServerParameters(
            command="python",
            args=["mcp_server/server.py"]
        )

        self.session = None
        self.tools = []
        self._stdio = None
        self._session_ctx = None

    async def connect(self):
        if self.session:
            return

        self._stdio = stdio_client(self.server_params)
        read, write = await self._stdio.__aenter__()

        self._session_ctx = ClientSession(read, write)
        self.session = await self._session_ctx.__aenter__()

        await self.session.initialize()

        response = await self.session.list_tools()
        self.tools = response.tools

    async def call_tool(self, tool_name, arguments):
        if not self.session:
            await self.connect()

        return await self.session.call_tool(tool_name, arguments)