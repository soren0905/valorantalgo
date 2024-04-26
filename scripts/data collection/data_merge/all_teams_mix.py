import pandas as pd
import json
import os

def combine_json_files(directory):
    combined_data = []
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as file:
                data = json.load(file)
                combined_data.extend(data)
    return combined_data

def combine_csv_files(directory):
    combined_df = pd.DataFrame()
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            filepath = os.path.join(directory, filename)
            df = pd.read_csv(filepath)
            combined_df = pd.concat([combined_df, df], ignore_index=True)
    return combined_df

def save_data_to_json(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Data saved to JSON file at: {filename}")

def save_data_to_csv(dataframe, filename):
    dataframe.to_csv(filename, index=False)
    print(f"Data saved to CSV file at: {filename}")

def main():
    json_directory = r'C:\Users\soren\Projects\ValAlgo\data\JSON\all teams'  # Update your path
    csv_directory = r'C:\Users\soren\Projects\ValAlgo\data\CSV\all teams'    # Update your path
    combined_json = combine_json_files(json_directory)
    combined_csv = combine_csv_files(csv_directory)

    # Save the combined data
    save_data_to_json(combined_json, os.path.join(json_directory, 'all_teams.json'))
    save_data_to_csv(combined_csv, os.path.join(csv_directory, 'all_teams.csv'))

if __name__ == '__main__':
    main()
