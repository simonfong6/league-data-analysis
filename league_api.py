import requests

CHAMPION_URL = 'http://ddragon.leagueoflegends.com/cdn/10.23.1/data/en_US/champion.json'

def create_champion_dict():
    response = requests.get(CHAMPION_URL)
    data = response.json()

    champion_list = data['data']

    champion_id_to_champion = {champion['key']: champion for name, champion in champion_list.items()}

    return champion_id_to_champion
