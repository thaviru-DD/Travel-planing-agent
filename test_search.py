import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

tavily_client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)

response = tavily_client.search(
    "best tourist attractions in Kandy Sri Lanka"
)

print(response)