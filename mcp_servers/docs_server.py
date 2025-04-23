from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv()
mcp = FastMCP("Docs")


### Resources for the server
# Obs: Resources are how you expose data to LLMs. They're similar to GET endpoints in a REST API - they provide data but
# shouldn't perform significant computation or have side effects:
@mcp.resource("info://sources/weather")
def get_weather_source() -> str:
    """Where the weather information is coming from"""
    return "The weather information is coming from https://www.weatherapi.com/"


@mcp.resource("info://sources/project_motivation")
def get_project_source() -> str:
    """Information about the project"""
    return "The main motivation of this project is to learn how to use MCP"


@mcp.resource("info://sources/project_repository")
def get_author_source() -> str:
    """Where is the project repository"""
    return "The project repository is on GitHub at https://github.com/Gbrlmoraes/mcp_sandbox"


### Runs the MCP server
# OBS:
# - transport="stdio" : (Standard Input/Output) Transport is primarily used for inter-process communication
# within the same system. To use this you will have to use the absolute path of the server in the command line.
# Ex: \mcp_testing\mcp_servers\weather_server.py

# - transport="sse" : ​Server-Sent Events (SSE) is a technology that enables servers to push real-time updates
# to web clients over a single, long-lived HTTP connection. To use this you will have to use the http url created
# by the server in the command line. Ex: http://0.0.0.0:8000
if __name__ == "__main__":
    mcp.run(transport="stdio")
