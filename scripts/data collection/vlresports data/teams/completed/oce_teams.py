import requests
import pandas as pd
import json
import os

def fetch_all_teams():
    base_url = "http://localhost:5000/api/v1/teams"
    all_teams = []
    page = 1
    has_next_page = True

    while has_next_page:
        # Set the region parameter to 'oce' to fetch only Oceania teams
        url = f"{base_url}?limit=50&page={page}&region=oce"  # Adjust limit to a safe value for pagination
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            all_teams.extend(data['data'])
            has_next_page = data['pagination']['hasNextPage']
            page += 1
        else:
            print(f"Failed to fetch data: {response.status_code}")
            break

    return all_teams

def save_data_to_json(teams):
    json_path = os.path.abspath('../../../../../data/JSON/all teams/oce_teams.json')  # Specify file for OCE teams
    os.makedirs(os.path.dirname(json_path), exist_ok=True)
    cleaned_teams = [{'id': team['id'], 'name': team['name'], 'country': team['country']} for team in teams]
    with open(json_path, 'w') as file:
        json.dump(cleaned_teams, file, indent=4)
    print("Data saved to JSON file at:", json_path)

def save_data_to_csv(teams):
    csv_path = os.path.abspath('../../../../../data/CSV/all teams/oce_teams.csv')  # Specify file for OCE teams
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    cleaned_teams = [{'id': team['id'], 'name': team['name'], 'country': team['country']} for team in teams]
    df = pd.DataFrame(cleaned_teams)
    df.to_csv(csv_path, index=False)
    print("Data saved to CSV file at:", csv_path)

def main():
    teams = fetch_all_teams()
    save_data_to_json(teams)
    save_data_to_csv(teams)

if __name__ == '__main__':
    main()
