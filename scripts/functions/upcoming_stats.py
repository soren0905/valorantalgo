import json
import os
import pandas as pd

def load_data(json_path):
    """ Load JSON data from a given file path. """
    print(f"Attempting to load data from: {json_path}")  # Debug: print the path
    if not os.path.exists(json_path):
        print(f"File does not exist: {json_path}")  # Debug: confirm if file exists
        return {}  # Return an empty dictionary instead of None
    with open(json_path, 'r', encoding='utf-8') as file:
        return json.load(file)



def combine_upcoming_with_stats(upcoming_players_path, combined_stats_path):
    upcoming_players = load_data(upcoming_players_path)
    combined_stats = load_data(combined_stats_path)

    if not combined_stats:  # Check if combined_stats is empty
        print("No combined stats data available.")
        return upcoming_players  # Return the upcoming players without modification

    # Get a list of all possible stats from the combined stats dictionary by checking the first player
    all_stat_keys = set()
    for stats in combined_stats.values():
        all_stat_keys.update(stats.keys())

    for team in upcoming_players:
        for player in team['players']:
            player_name = player['user']
            player_stats = combined_stats.get(player_name, {})

            # Ensure each map stat is present, if not, initialize it with zero values
            for map_stat in all_stat_keys:
                if map_stat not in player_stats:
                    player_stats[map_stat] = {'RND': 0, 'KPR': 0, 'APR': 0, 'FKPR': 0, 'KMAX': 0}

            player.update(player_stats)

    return upcoming_players


def save_data(data, json_path, csv_path):
    with open(json_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

    # Flatten the data for CSV output
    df = pd.DataFrame([item for sublist in [team['players'] for team in data] for item in sublist])
    df.to_csv(csv_path, index=False)
    print(f"Data saved to JSON and CSV files at: {json_path} and {csv_path}")

def main():
    project_root = r'C:\Users\soren\Projects\ValAlgo'
    upcoming_players_path = os.path.join(project_root, 'data', 'JSON', 'upcoming_players.json')
    combined_stats_path = os.path.join(project_root, 'data', 'JSON', 'map_stats', 'combined_map_stats.json')
    output_json_path = os.path.join(project_root, 'data', 'JSON', 'upcoming_with_stats.json')
    output_csv_path = os.path.join(project_root, 'data', 'CSV', 'upcoming_with_stats.csv')

    print(f"Checking paths:\nUpcoming: {upcoming_players_path}\nCombined: {combined_stats_path}")  # Debugging

    combined_data = combine_upcoming_with_stats(upcoming_players_path, combined_stats_path)
    if combined_data is not None:
        save_data(combined_data, output_json_path, output_csv_path)

if __name__ == '__main__':
    main()







