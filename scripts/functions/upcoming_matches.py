import requests
import pandas as pd
import json
import os


def fetch_upcoming_matches():
    url = 'http://localhost:5000/api/v1/matches'  # Replace with the correct URL if needed
    response = requests.get(url)
    if response.status_code == 200:
        matches = response.json().get('data', [])
        print("Fetched data:", matches)  # Debugging print statement
        return matches
    else:
        print("Failed to fetch matches. Status code:", response.status_code)  # Error information
        return []


def save_data_to_json(matches):
    json_path = r'C:\Users\soren\Projects\ValAlgo\data\JSON\upcoming_matches.json'
    os.makedirs(os.path.dirname(json_path), exist_ok=True)

    # Additional filter to exclude matches with "TBD" status or teams
    processed_json_data = [
        {
            'id': match['id'],
            'teams': [{'name': team['name']} for team in match['teams'] if team['name'] != 'TBD'],
            'status': match['status']
        }
        for match in matches
        if match['status'] != 'TBD' and all(team['name'] != 'TBD' for team in match['teams'])
    ]
    print("Filtered JSON data:", processed_json_data)  # Debugging print statement
    if processed_json_data:
        with open(json_path, 'w') as json_file:
            json.dump(processed_json_data, json_file, indent=4)
        print("Data saved to JSON file at:", json_path)
    else:
        print("No valid data to save to JSON.")


def save_data_to_csv(matches):
    csv_path = r'C:\Users\soren\Projects\ValAlgo\data\CSV\upcoming_matches.csv'
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)

    processed_csv_data = [
        {
            'teams': ', '.join([team['name'] for team in match['teams'] if team['name'] != 'TBD']),
            'status': match['status']
        }
        for match in matches
        if match['status'] != 'TBD' and all(team['name'] != 'TBD' for team in match['teams'])
    ]
    print("Filtered CSV data:", processed_csv_data)  # Debugging print statement
    if processed_csv_data:
        df = pd.DataFrame(processed_csv_data)
        df.to_csv(csv_path, index=False)
        print("Data saved to CSV file at:", csv_path)
    else:
        print("No valid data to save to CSV.")


def main():
    matches = fetch_upcoming_matches()
    save_data_to_json(matches)
    save_data_to_csv(matches)


if __name__ == '__main__':
    main()










