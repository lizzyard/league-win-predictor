import json
import os
import pandas as pd

RAW_DATA_DIR = "data/raw"
PROCESSED_DATA_DIR = "data/processed"
OUTPUT_FILE = "data/processed/timeline_15_features.csv"

TARGET_MINUTE = 15

def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)
    
def extract_15_min_features(timeline_data, match_data):
    match_id = match_data["metadata"]["matchId"]

    frames = timeline_data["info"]["frames"]

    if len(frames) <= TARGET_MINUTE:
        return []
    
    frame = frames[TARGET_MINUTE]

    participant_frames = frame["participantFrames"]

    teams = {
        100: {
            "match_id": match_id,
            "team_id": 100,
            "gold": 0,
            "xp": 0,
            "cs": 0,
            "win": False,
        },
        200: {
            "match_id": match_id,
            "team_id": 200,
            "gold": 0,
            "xp": 0,
            "cs": 0,
            "win": False,
        },
    }

    participants = match_data["info"]["participants"]

    wins = [player["win"] for player in participants]


    if wins.count(True) != 5:
        print(f"Skipping {match_id}: invalid win data")
        return []

    for player in participants:
        participant_id = str(player["participantId"])


        participant_id = str(player["participantId"])
        team_id = player["teamId"]

        player_frame = participant_frames[participant_id]

        teams[team_id]["gold"] += player_frame["totalGold"]
        teams[team_id]["xp"] += player_frame["xp"]
        teams[team_id]["cs"] += (
            player_frame["minionsKilled"] + player_frame["jungleMinionsKilled"]
        )
        teams[team_id]["win"] = player["win"]

    blue = teams[100]
    red = teams[200]

    return [
        {
            "match_id": match_id,
            "team_id": 100,
            "gold_diff_15": blue["gold"] - red["gold"],
            "xp_diff_15": blue["xp"] - red["xp"],
            "cs_diff_15": blue["cs"] - red["cs"],
            "win": blue["win"],
        },
        {
            "match_id": match_id,
            "team_id": 200,
            "gold_diff_15": red["gold"] - blue["gold"],
            "xp_diff_15": red["xp"] - blue["xp"],
            "cs_diff_15": red["cs"] - blue["cs"],
            "win": red["win"],
        },
    ]

def main():
    all_rows = []

    for file_name in os.listdir(RAW_DATA_DIR):
        if file_name.endswith("_timeline.json"):
            match_id = file_name.replace("_timeline.json", "")

            timeline_path = os.path.join(RAW_DATA_DIR, file_name)
            match_path = os.path.join(RAW_DATA_DIR, f"{match_id}.json")

            if not os.path.exists(match_path):
                print(f"Skipping {match_id}: missing match file")
                continue

            timeline_data = load_json(timeline_path)
            match_data = load_json(match_path)

            if "info" not in timeline_data or "info" not in match_data:
                print(f"Skipping {match_id}: invalid file")
                continue

            rows = extract_15_min_features(timeline_data, match_data)
            all_rows.extend(rows)

    df = pd.DataFrame(all_rows)

    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)

    print(df)
    print(f"Saved timeline features to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()