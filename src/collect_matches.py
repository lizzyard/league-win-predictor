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
    os.makedirs("data/raw", exist_ok=True)

    file_path = f"data/raw/{match_id}.json"

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(match_data, file, indent=4)

    print(f"Saved match data to {file_path}")

def save_timeline_data(match_id, timeline_data):
    os.makedirs("data/raw", exist_ok=True)

    file_path = f"data/raw/{match_id}_timeline.json"

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(timeline_data, file, indent=4)

    print(f"Saved timeline data to {file_path}")

def download_matches(match_ids):
    os.makedirs("data/raw", exist_ok=True)

    for match_id in match_ids:
        match_path = f"data/raw/{match_id}.json"
        timeline_path = f"data/raw/{match_id}_timeline.json"

        match_exists = os.path.exists(match_path)
        timeline_exists = os.path.exists(timeline_path)

        if match_exists and timeline_exists:
            print(f"Skipping {match_id}: files already exist")
            continue

        print(f"Downloading {match_id}...")

        if not match_exists:
            match_data = get_match_data(match_id)
            save_match_data(match_id, match_data)
        else:
            print(f"Match file already exists: {match_path}")

        if not timeline_exists:
            timeline_data = get_match_timeline(match_id)
            save_timeline_data(match_id, timeline_data)
        else:
            print(f"Timeline file already exists: {timeline_path}")

        time.sleep(1)
        time.sleep(1)

def riot_get(url, max_retries=5):
    attempts = 0

    while attempts < max_retries:
        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code == 200:
            return response.json()

        if response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 60))
            attempts += 1

            print(
                f"Rate limit hit. Waiting {retry_after} seconds "
                f"(attempt {attempts}/{max_retries})..."
            )

            time.sleep(retry_after)
            continue

        raise Exception(
            f"Request failed: {response.status_code} {response.text}"
        )

    raise Exception("Maximum retry attempts reached.")


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




