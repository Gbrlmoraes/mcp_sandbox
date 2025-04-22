import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

from langchain_ollama import ChatOllama

model = ChatOllama(model="llama3.2:1b")


async def main(message: str):
    async with MultiServerMCPClient(
        {
            "weather": {
                "url": "http://localhost:8000/sse",
                "transport": "sse",
            }
        }
    ) as client:
        agent = create_react_agent(model, client.get_tools())
        messages = await agent.ainvoke({"messages": [("user", message)]})
        for m in messages["messages"]:
            m.pretty_print()


if __name__ == "__main__":
    asyncio.run(main("How's the weather and temperature in Ubajara?"))
