import requests
import pandas as pd
import json
import os


def fetch_upcoming_matches():
    url = 'http://localhost:5000/api/v1/matches'  # Replace with the correct URL if needed
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('data', [])
    else:
        return []


def save_data_to_json(matches):
    json_path = r'/data/JSON/upcoming_matches.json'
    # Filter out matches where any team is 'TBD'
    processed_json_data = [{
        'id': match['id'],
        'teams': [{'name': team['name']} for team in match['teams'] if team['name'] != 'TBD'],
        'status': match['status']
    } for match in matches if all(team['name'] != 'TBD' for team in match['teams'])]

    with open(json_path, 'w') as json_file:
        json.dump(processed_json_data, json_file, indent=4)
    print("Data saved to JSON file at:", json_path)


def save_data_to_csv(matches):
    csv_path = r'/data/CSV/upcoming_matches.csv'
    # Filter and format for CSV
    processed_csv_data = [{
        'teams': ', '.join([team['name'] for team in match['teams'] if team['name'] != 'TBD']),
        'status': match['status']
    } for match in matches if all(team['name'] != 'TBD' for team in match['teams'])]

    if processed_csv_data:  # Ensure there is data to convert
        df = pd.DataFrame(processed_csv_data)
        df.to_csv(csv_path, index=False)
        print("Data saved to CSV file at:", csv_path)
    else:
        print("No data available to save to CSV.")


def main():
    matches = fetch_upcoming_matches()
    save_data_to_json(matches)
    save_data_to_csv(matches)


if __name__ == '__main__':
    main()





