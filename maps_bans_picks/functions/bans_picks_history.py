import requests
from bs4 import BeautifulSoup
import json
import csv
import os


def load_json_data(file_path):
    """Load data from a JSON file."""
    with open(file_path, 'r') as file:
        return json.load(file)


def fetch_match_history(url):
    """Fetch and parse match history from the URL."""
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        match_note = soup.find('div', class_='match-header-note')
        return match_note.text.strip() if match_note else "No match history found"
    else:
        print(f"Failed to fetch page: HTTP {response.status_code}")
        return None


def save_to_json(data, filename):
    """Save data to a JSON file."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Data saved to {filename}")


def save_to_csv(data, filename):
    """Save data to a CSV file."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Match ID', 'Team ID', 'Team Name', 'Match URL', 'Match History'])
        for match_id, teams in data.items():
            for team in teams:
                writer.writerow([match_id, team['id'], team['name'], team['match_url'], team['history']])


def main():
    json_path = r'C:\Users\soren\Projects\ValAlgo\data\JSON\upcoming_match_history.json'
    matches = load_json_data(json_path)

    match_histories = {}
    for match_id, teams in matches.items():
        team_data = []
        for team in teams:
            team_name = team['name']
            team_id = team['id']
            for result in team['details']['results']:
                match_url = result['match_url']
                history = fetch_match_history(match_url)
                result['history'] = history
                team_data.append({'id': team_id, 'name': team_name, 'match_url': match_url, 'history': history})
        match_histories[match_id] = team_data

    json_output_path = r'C:\Users\soren\Projects\ValAlgo\data\JSON\match_histories.json'
    csv_output_path = r'C:\Users\soren\Projects\ValAlgo\data\CSV\match_histories.csv'
    save_to_json(match_histories, json_output_path)
    save_to_csv(match_histories, csv_output_path)


if __name__ == '__main__':
    main()




