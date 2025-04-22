import httpx
import os
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv()
mcp = FastMCP("Weather")


### Tools for the server
# OBS: Tools let LLMs take actions through your server. Unlike resources, tools are expected
# to perform computation and have side effects
@mcp.tool()
async def get_weather_information(city: str) -> str:
    """Fetch current weather for a city"""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.weatherapi.com/v1/current.json?key={os.getenv('WEATHER_API_KEY')}&q={city}&aqi=no"
        )
        location_info = response.json()["location"]
        weather_info = response.json()["current"]

        return f"The up-to-date weather information is: City: {location_info['name']}, Region: {location_info['region']}, Country: {location_info['country']}, Temperature: {weather_info['temp_c']}°C, Condition: {weather_info['condition']['text']}"


### Runs the MCP server
# OBS:
# - transport="stdio" : (Standard Input/Output) Transport is primarily used for inter-process communication
# within the same system. To use this you will have to use the absolute path of the server in the command line.
# Ex: \mcp_testing\mcp_servers\weather_server.py

# - transport="sse" : ​Server-Sent Events (SSE) is a technology that enables servers to push real-time updates
# to web clients over a single, long-lived HTTP connection. To use this you will have to use the http url created
# by the server in the command line. Ex: http://0.0.0.0:8000
if __name__ == "__main__":
    mcp.run(transport="sse")
