import pandas as pd
import json
import os

def load_data(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)

def combine_player_stats(map_stats_directory):
    map_files = [f for f in os.listdir(map_stats_directory) if f.endswith('.json')]
    combined_stats = {}

    for map_file in map_files:
        map_name = map_file.replace('.json', '')
        map_stats = load_data(os.path.join(map_stats_directory, map_file))

        for stat in map_stats:
            try:
                player_name = stat['Player'].split('\n')[0]
                if player_name not in combined_stats:
                    combined_stats[player_name] = {}
                combined_stats[player_name][map_name] = {
                    'RND': stat.get('RND'),
                    'KPR': stat.get('KPR'),
                    'APR': stat.get('APR'),
                    'FKPR': stat.get('FKPR'),
                    'KMAX': stat.get('KMAX')
                }
            except TypeError:
                print(f"Error processing data: {stat}")
                continue

    return combined_stats

def save_data_to_json(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Data saved to JSON file at: {filename}")

def save_data_to_csv(data, filename):
    dataframe = pd.DataFrame.from_dict({(i,j): data[i][j]
                                       for i in data.keys()
                                       for j in data[i].keys()},
                                       orient='index')
    dataframe.to_csv(filename, index=True)
    print(f"Data saved to CSV file at: {filename}")

def main():
    map_stats_directory = r'C:\Users\soren\Projects\ValAlgo\data\JSON\map_stats'
    combined_stats = combine_player_stats(map_stats_directory)

    json_output = os.path.join(map_stats_directory, 'combined_map_stats.json')
    csv_output = os.path.join(map_stats_directory.replace('JSON', 'CSV'), 'combined_map_stats.csv')
    save_data_to_json(combined_stats, json_output)
    save_data_to_csv(combined_stats, csv_output)

if __name__ == '__main__':
    main()









