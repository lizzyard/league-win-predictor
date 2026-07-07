import os
import requests
from dotenv import load_dotenv
import json
import time


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

    return riot_get(url)["puuid"]

def get_match_ids(puuid, count=50):
    url = (
        f"https://americas.api.riotgames.com/"
        f"lol/match/v5/matches/by-puuid/"
        f"{puuid}/ids"
        f"?start=0&count={count}"
    )
    
    return riot_get(url)

def get_match_data(match_id):
    url = (
        f"https://americas.api.riotgames.com/"
        f"lol/match/v5/matches/"
        f"{match_id}"
    )

    return riot_get(url)



def get_match_timeline(match_id):
    url = (
        f"https://americas.api.riotgames.com/"
        f"lol/match/v5/matches/"
        f"{match_id}/timeline"
    )
    
    return riot_get(url)

def save_match_data(match_id, match_data):
    file_path = f"data/raw/{match_id}.json"

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(match_data, file, indent=4)

    print(f"Saved match data to {file_path}")

def save_timeline_data(match_id, timeline_data):
    file_path = f"data/raw/{match_id}_timeline.json"

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(timeline_data, file, indent=4)
    
    print(f"Saved timeline data to {file_path}")

def download_matches(match_ids):
    for match_id in match_ids:
        print(f"Downloading {match_id}...")

        match_data = get_match_data(match_id)

        if match_data is None:
            continue

    save_match_data(match_id, match_data)

    timeline_data = get_match_timeline(match_id)
    save_timeline_data(match_id, timeline_data)

def riot_get(url):
    while True:
        response = requests.get(url, headers=headers)

        if response.status_code == 429:
            print("Rate limit hit. Waiting 15 seconds...")
            time.sleep(15)
            continue
        if response.status_code != 200:
            raise Exception(f"Request failed: {response.status_code} {response.json()}")
        return response.json()


PLAYERS = [
    ("ZOMBIE","十十十"),
]

MATCH_COUNT = 50

def main():
    all_match_ids = set()

    for game_name, tag_line, in PLAYERS:
        print(f"Getting matches for {game_name}#{tag_line}")

        puuid = get_puuid(game_name,tag_line)
        match_ids = get_match_ids(puuid, count=MATCH_COUNT)

        for match_id in match_ids:
            all_match_ids.add(match_id)

    download_matches(list(all_match_ids))

if __name__ == "__main__":
    main()




