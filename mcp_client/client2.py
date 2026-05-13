import asyncio
from mcp import ClientSession
from mcp.client.stdio import stdio_client,StdioServerParameters
import concurrent.futures

class MCPToolClient:
    def __init__(self):
        self.server_params = StdioServerParameters(
            command="python",
            args=["mcp_server/server.py"]
        )
        self.session = None
        self._stdio_ctx = None
        self._session_ctx = None

    async def connect(self):
        self._stdio_ctx = stdio_client(self.server_params)
        read, write = await self._stdio_ctx.__aenter__()

        self._session_ctx = ClientSession(read, write)
        self.session = await self._session_ctx.__aenter__()

        await self.session.initialize()

    async def call_tool(self, tool_name: str, arguments: dict):
        if not self.session:
            await self.connect()

        return await self.session.call_tool(tool_name, arguments)

    async def close(self):
        if self._session_ctx:
            await self._session_ctx.__aexit__(None, None, None)

        if self._stdio_ctx:
            await self._stdio_ctx.__aexit__(None, None, None)


    async def call_tool_async(self, tool_name: str, arguments: dict):
        async with stdio_client(self.server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                result = await session.call_tool(tool_name, arguments)
                return result

    def call_tool_sync(self, tool_name: str, arguments: dict):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            return asyncio.run(self.call_tool_async(tool_name, arguments))
        
        with concurrent.futures.ThreadPoolExecutor() as pool:
            return pool.submit(
                asyncio.run, self._call_tool_async(tool_name, arguments)
            ).result()

client = MCPToolClient()