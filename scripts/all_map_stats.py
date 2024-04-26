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
    os.makedirs(os.path.dirname(json_path), exist_ok=True)
    with open(json_path, 'w') as json_file:
        json.dump(players_data, json_file, indent=4)

    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    df = pd.DataFrame(players_data)
    df.to_csv(csv_path, index=False)
    print(f"Data saved to JSON and CSV files at {json_path} and {csv_path}.")

def main():
    maps = {
        "ascent": "https://www.vlr.gg/stats/?event_group_id=all&event_id=all&region=all&country=all&min_rounds=0&min_rating=1550&agent=all&map_id=5&timespan=60d",
        "bind": "https://www.vlr.gg/stats/?event_group_id=all&event_id=all&region=all&country=all&min_rounds=0&min_rating=1550&agent=all&map_id=1&timespan=60d",
        "breeze": "https://www.vlr.gg/stats/?event_group_id=all&event_id=all&region=all&country=all&min_rounds=0&min_rating=1550&agent=all&map_id=8&timespan=60d",
        "icebox": "https://www.vlr.gg/stats/?event_group_id=all&event_id=all&region=all&country=all&min_rounds=0&min_rating=1550&agent=all&map_id=6&timespan=60d",
        "lotus": "https://www.vlr.gg/stats/?event_group_id=all&event_id=all&region=all&country=all&min_rounds=0&min_rating=1550&agent=all&map_id=11&timespan=60d",
        "split": "https://www.vlr.gg/stats/?event_group_id=all&event_id=all&region=all&country=all&min_rounds=0&min_rating=1550&agent=all&map_id=3&timespan=60d",
        "sunset": "https://www.vlr.gg/stats/?event_group_id=all&event_id=all&region=all&country=all&min_rounds=0&min_rating=1550&agent=all&map_id=12&timespan=60d"
    }

    for map_name, url in maps.items():
        player_stats = fetch_player_stats(url)
        base_dir = os.path.abspath(os.path.dirname(__file__))
        json_path = os.path.join(base_dir, f'data/JSON/{map_name}_stats.json')
        csv_path = os.path.join(base_dir, f'data/CSV/{map_name}_stats.csv')
        save_data(player_stats, json_path, csv_path)

if __name__ == '__main__':
    main()

