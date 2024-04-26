import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import os


def fetch_player_stats(url):
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to fetch webpage")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', {'class': 'wf-table mod-stats mod-scroll'})
    rows = table.find('tbody').find_all('tr')

    players_data = []
    for row in rows:
        cols = row.find_all('td')
        if 'TBD' in [col.text.strip() for col in cols]:
            continue  # Skip rows where a player name is "TBD"
        player_data = {
            'Player': cols[0].text.strip(),
            'RND': cols[2].text.strip(),
            'KPR': cols[8].text.strip(),
            'APR': cols[9].text.strip(),
            'FKPR': cols[10].text.strip(),
            'KMAX': cols[15].text.strip()
        }
        players_data.append(player_data)

    return players_data


def save_data(players_data, json_path, csv_path):
    os.makedirs(os.path.dirname(json_path), exist_ok=True)  # Ensure the directory exists
    with open(json_path, 'w') as json_file:
        json.dump(players_data, json_file, indent=4)

    os.makedirs(os.path.dirname(csv_path), exist_ok=True)  # Ensure the directory exists
    df = pd.DataFrame(players_data)
    df.to_csv(csv_path, index=False)
    print("Data saved to JSON and CSV files.")


def main():
    url = 'https://www.vlr.gg/stats/?event_group_id=all&event_id=all&region=all&country=all&min_rounds=0&min_rating=1550&agent=all&map_id=5&timespan=60d'
    json_path = r'/data/JSON/map_stats/bind_stats.json'
    csv_path = r'../../../data/CSV/map_stats/bind_stats.csv'

    player_stats = fetch_player_stats(url)
    save_data(player_stats, json_path, csv_path)


if __name__ == '__main__':
    main()

