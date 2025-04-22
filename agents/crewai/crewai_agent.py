from crewai import Agent, Crew, Task, LLM
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from crewai_tools import MCPServerAdapter

load_dotenv()


class WeatherReportOutput(BaseModel):
    report: str
    temperature: str
    condition: str


agents_config = os.path.join(os.path.dirname(__file__), "config", "agents.yaml")
tasks_config = os.path.join(os.path.dirname(__file__), "config", "tasks.yaml")

llm = LLM(model="ollama/llama3.2:1b", temperature=0, seed=42)

serverparams = {"url": "http://localhost:8000/sse"}

try:
    mcp_server_adapter = MCPServerAdapter(serverparams)  # Starts the server

    tools = (
        mcp_server_adapter.tools
    )  # tools is now a list of CrewAI Tools matching 1:1 with the MCP server's tools

    agent = Agent(
        config=agents_config["weather_broadcaster"], verbose=True, llm=llm, tools=tools
    )

    task = Task(
        config=tasks_config["give_weather_report"],
        agent=agent,
        output_pydantic=WeatherReportOutput,
        tools=tools,
        llm=llm,
    )

    crew = Crew(agents=[agent], tasks=[task])
    result = crew.kickoff(
        inputs={
            "question": "How's the weather and temperature in Ubajara?",
        }
    ).pydantic.model_dump()

    print("Report:", result["report"], "\n")
    print("Temperature:", result["temperature"], "\n")
    print("Condition:", result["condition"], "\n")

# Stops the server even if the agent fails
finally:
    mcp_server_adapter.stop()
