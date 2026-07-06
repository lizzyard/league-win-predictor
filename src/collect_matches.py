import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("RIOT_API_KEY")

if API_KEY is None:
    raise ValueError("RIOT_API_KEY not found. Check your .env file.")

print("API Key loaded succesfully.")

headers = {
    "X-Riot-Token": API_KEY
}

url = "https://na1.api.riotgames.com/lol/status/v4/platform-data"

response = requests.get(url, headers=headers)

print("Status code:", response.status_code)
print(response.json())