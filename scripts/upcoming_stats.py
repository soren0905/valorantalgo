import json
import os
import pandas as pd


def load_data(json_path):
    with open(json_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def combine_upcoming_with_stats(upcoming_players_path, combined_stats_path):
    upcoming_players = load_data(upcoming_players_path)
    combined_stats = load_data(combined_stats_path)

    for team in upcoming_players:
        for player in team['players']:
            player_name = player['user']
            player_stats = combined_stats.get(player_name)
            if player_stats:
                player.update(player_stats)
            else:
                # If no stats are found for a player, you might want to handle this case, e.g., log it or set default values
                player.update({map_stat: None for map_stat in combined_stats[next(iter(combined_stats))].keys()})

    return upcoming_players


def save_data(data, json_path, csv_path):
    with open(json_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

    df = pd.DataFrame([item for sublist in [team['players'] for team in data] for item in sublist])
    df.to_csv(csv_path, index=False)
    print(f"Data saved to JSON and CSV files at: {json_path} and {csv_path}")


def main():
    project_root = r'C:\Users\soren\Projects\ValAlgo'  # Base path for the project
    upcoming_players_path = os.path.join(project_root, 'data', 'JSON', 'upcoming_players.json')
    combined_stats_path = os.path.join(project_root, 'data', 'JSON', 'combined_map_stats.json')
    output_json_path = os.path.join(project_root, 'data', 'JSON', 'upcoming_with_stats.json')
    output_csv_path = os.path.join(project_root, 'data', 'CSV', 'upcoming_with_stats.csv')

    combined_data = combine_upcoming_with_stats(upcoming_players_path, combined_stats_path)
    save_data(combined_data, output_json_path, output_csv_path)


if __name__ == '__main__':
    main()





