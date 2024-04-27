import requests
import json
import os
import csv

def load_json_data(file_path):
    """Load data from a JSON file."""
    with open(file_path, 'r') as file:
        return json.load(file)

def fetch_team_details(team_id):
    """Fetch detailed information for a specific team by its ID using an API."""
    url = f"http://localhost:5000/api/v1/teams/{team_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return filter_team_details(response.json())
    else:
        print(f"Failed to fetch team data for ID {team_id}: HTTP {response.status_code}")
        return None

def filter_team_details(team_details):
    """Limit and remove unwanted nested keys from team details."""
    filtered_details = {}
    if 'data' in team_details and 'results' in team_details['data']:
        # Limit to the first 7 matches only
        limited_results = team_details['data']['results'][:7]
        filtered_details['results'] = [{
            'match_id': result['match']['id'],
            'match_url': result['match']['url']
        } for result in limited_results if 'match' in result]
    return filtered_details

def group_teams_by_match(upcoming_matches, all_teams):
    """Extract and group team details by match ID using team names."""
    team_id_map = {team['name']: team['id'] for team in all_teams}
    matches = {}
    for match in upcoming_matches:
        match_id = match['id']
        teams = []
        for team in match['teams']:
            team_name = team['name']
            team_id = team_id_map.get(team_name)
            if team_id:
                team_details = fetch_team_details(team_id)
                if team_details:
                    teams.append({'id': team_id, 'name': team_name, 'details': team_details})
                else:
                    teams.append({'id': team_id, 'name': team_name, 'details': 'No data available'})
            else:
                print(f"Team named '{team_name}' not found in all_teams data.")
        matches[match_id] = teams
    return matches

def save_data_to_json(data, filename):
    """Save data to a JSON file."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Data saved to {filename}")

def save_data_to_csv(data, filename):
    """Save data to a CSV file."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Match ID', 'Team ID', 'Team Name', 'Match ID', 'Match URL'])
        for match_id, teams in data.items():
            for team in teams:
                for detail in team.get('details', {}).get('results', []):
                    writer.writerow([match_id, team['id'], team['name'], detail['match_id'], detail['match_url']])

    print(f"Data saved to {filename}")

def main():
    upcoming_matches_path = r'C:\Users\soren\Projects\ValAlgo\data\JSON\upcoming_matches.json'
    all_teams_path = r'C:\Users\soren\Projects\ValAlgo\data\JSON\all_teams.json'

    upcoming_matches = load_json_data(upcoming_matches_path)
    all_teams = load_json_data(all_teams_path)

    # Process and group team details by match ID
    grouped_teams = group_teams_by_match(upcoming_matches, all_teams)

    # Save the data to JSON
    json_filename = r'C:\Users\soren\Projects\ValAlgo\data\JSON\filtered_team_details.json'
    save_data_to_json(grouped_teams, json_filename)

    # Save the data to CSV
    csv_filename = r'C:\Users\soren\Projects\ValAlgo\data\CSV\filtered_team_details.csv'
    save_data_to_csv(grouped_teams, csv_filename)

if __name__ == '__main__':
    main()


