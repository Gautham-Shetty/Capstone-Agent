from fastmcp import FastMCP
import httpx

mcp = FastMCP("random-facts")

@mcp.tool()
async def get_joke()->str:
    url="https://official-joke-api.appspot.com/random_joke"
    print("hereee  ")
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
        print(f"Joke of the day {data['setup']} - {data['punchline']}")
        return f"Joke of the day {data['setup']} - {data['punchline']}"