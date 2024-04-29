import requests
import pandas as pd
import json
import os

def load_data(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return []
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def fetch_team_details(team_id):
    url = f'http://localhost:5000/api/v1/teams/{team_id}'
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None

def clean_data(team_details):
    # Clean the team details for both JSON and CSV
    cleaned_data = []
    for details in team_details:
        team_info = {
            "info": {
                "name": details['data']['info']['name'],
            },
            "players": [{"id": player["id"], "user": player["user"]} for player in details['data']['players']]
        }
        cleaned_data.append(team_info)
    return cleaned_data

def save_data(data, json_path, csv_path):
    with open(json_path, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Data saved to JSON file at: {json_path}")

    if data:  # Ensure there's data
        df = pd.json_normalize(data, record_path=['players'], meta=[['info', 'name']], errors='ignore')
        df.to_csv(csv_path, index=False)
        print(f"Data saved to CSV file at: {csv_path}")
    else:
        print("No data to save to CSV.")

def main():
    # Use the correct directory path directly
    data_dir = 'C:\\Users\\soren\\Projects\\ValAlgo\\data'  # Windows path with escaped backslashes

    json_path = os.path.join(data_dir, 'JSON', 'upcoming_players.json')
    csv_path = os.path.join(data_dir, 'CSV', 'upcoming_players.csv')

    upcoming_matches_path = os.path.join(data_dir, 'JSON', 'upcoming_matches.json')
    all_teams_path = os.path.join(data_dir, 'JSON', 'all_teams.json')

    # Load data from JSON files
    upcoming_matches = load_data(upcoming_matches_path)
    all_teams = load_data(all_teams_path)
    if not upcoming_matches or not all_teams:
        return  # Exit if data could not be loaded


    team_name_to_id = {team['name']: team['id'] for team in all_teams}

    # Process upcoming matches
    print("Processing upcoming matches:", len(upcoming_matches))

    team_details = []
    for match in upcoming_matches:
        for team in match.get('teams', []):  # Ensure 'teams' key exists
            team_name = team.get('name')
            team_id = team_name_to_id.get(team_name)
            if team_id:
                details = fetch_team_details(team_id)
                if details:
                    team_details.append(details)
                else:
                    print(f"Failed to fetch details for team ID: {team_id}")
            else:
                print(f"No ID found for team: {team_name}")

    # Clean and save data
    cleaned_data = clean_data(team_details)
    save_data(cleaned_data, json_path, csv_path)

if __name__ == '__main__':
    main()

