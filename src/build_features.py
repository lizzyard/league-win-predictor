import json
import os 
import pandas as pd 

RAW_DATA_DIR = "data/raw"
PROCESSED_DATA_DIR = "data/processed"
OUTPUT_FILE = "data/processed/team_features.csv"

def load_match_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

def extract_team_features(match_data):
    participants = match_data["info"]["participants"]
    match_id = match_data["metadata"]["matchId"]

    teams = {
        100: {
            "match_id": match_id,
            "team_id": 100,
            "total_gold": 0,
            "kills": 0,
            "deaths": 0,
            "assists": 0,
            "cs": 0,
            "vision_score": 0,
            "win": False,
        },
        200: {
            "match_id": match_id,
            "team_id": 200,
            "total_gold": 0,
            "kills": 0,
            "deaths": 0,
            "assists": 0,
            "cs": 0,
            "vision_score": 0,
            "win": False,
        },
    }

    for player in participants:
        team_id = player["teamId"]

        teams[team_id]["total_gold"] += player["goldEarned"]
        teams[team_id]["kills"] += player["kills"]
        teams[team_id]["deaths"] += player["deaths"]
        teams[team_id]["assists"] += player["assists"]
        teams[team_id]["cs"] += (
            player["totalMinionsKilled"] + player["neutralMinionsKilled"]
        )
        teams[team_id]["vision_score"] += player["visionScore"]
        teams[team_id]["win"] = player["win"]
    return list(teams.values())

def main():
    all_rows = []
    
    for file_name in os.listdir(RAW_DATA_DIR):
        if file_name.endswith(".json"):
            file_path = os.path.join(RAW_DATA_DIR, file_name)
            match_data = load_match_file(file_path)

            team_rows = extract_team_features(match_data)
            all_rows.extend(team_rows)

    df = pd.DataFrame(all_rows)
    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)
    print(df)
    print(f"Saved features to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()