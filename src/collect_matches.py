import os
import requests
from dotenv import load_dotenv
import json

load_dotenv()

API_KEY = os.getenv("RIOT_API_KEY")

if API_KEY is None:
    raise ValueError("RIOT_API_KEY not found. Check your .env file.")

headers = {
    "X-Riot-Token": API_KEY
}


def get_puuid(game_name, tag_line):
    url = (
        f"https://americas.api.riotgames.com/"
        f"riot/account/v1/accounts/by-riot-id/"
        f"{game_name}/{tag_line}"
    )

    response = requests.get(url, headers=headers)

    print("Status code:", response.status_code)
    print(response.json())

    data = response.json()
    return data["puuid"]

def get_match_ids(puuid, count=5):
    url = (
        f"https://americas.api.riotgames.com/"
        f"lol/match/v5/matches/by-puuid/"
        f"{puuid}/ids"
        f"?start=0&count={count}"
    )
    response = requests.get(url, headers=headers)
    print("Match IDs status code:", response.status_code)
    print(response.json())

    return response.json()

def get_match_data(match_id):
    url = (
        f"https://americas.api.riotgames.com/"
        f"lol/match/v5/matches/"
        f"{match_id}"
    )

    response = requests.get(url, headers=headers)

    print("Match data status code:", response.status_code)
    return response.json()

def save_match_data(match_id, match_data):
    file_path = f"data/raw/{match_id}.json"

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(match_data, file, indent=4)

    print(f"Saved match data to {file_path}")

def download_matches(match_ids):
    for match_id in match_ids:
        print(f"Downloading {match_id}...")

        match_data = get_match_data(match_id)
        save_match_data(match_id, match_data)

# example
puuid = get_puuid("ZOMBIE", "十十十")
match_ids = get_match_ids(puuid, count=50)

download_matches(match_ids)






