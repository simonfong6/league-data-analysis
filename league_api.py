import requests
from functools import lru_cache

from IPython.core.display import display
from IPython.core.display import HTML

CHAMPION_URL = 'http://ddragon.leagueoflegends.com/cdn/10.22.1/data/en_US/champion.json'

ITEM_URL = 'http://ddragon.leagueoflegends.com/cdn/10.22.1/data/en_US/item.json'

@lru_cache(None)
def create_champion_dict(patch_version='10.22.1'):
    print("Creating champion dictionary.")
    response = requests.get(CHAMPION_URL)
    data = response.json()

    champion_list = data['data']

    champion_id_to_champion = {int(champion['key']): champion for name, champion in champion_list.items()}

    return champion_id_to_champion

@lru_cache(None)
def create_champion_name_to_champion_id_map(patch_version='10.22.1'):
    response = requests.get(CHAMPION_URL)
    data = response.json()

    champion_list = data['data']

    champion_name_to_champion_id = {champion['id']: int(champion['key']) for name, champion in champion_list.items()}

    return champion_name_to_champion_id

def convert_champion_name_to_id(name, name_id_map=None):
    if name_id_map is None:
        name_id_map = create_champion_name_to_champion_id_map()
    return name_id_map[name]

@lru_cache(None)
def create_item_map(patch_version='10.22.1'):
    response = requests.get(ITEM_URL)
    data = response.json()
    item_map = data['data']

    return item_map

def create_item_name_to_id_map():
    item_map = create_item_map()

    item_name_to_id_map = {item['name']: int(id) for id, item in item_map.items()}

    return item_name_to_id_map

def convert_item_name_to_id(name, name_id_map=None):
    if name_id_map is None:
        name_id_map = create_item_name_to_id_map()
    return name_id_map[name]

def display_item(item_id):
    image_url = f'http://ddragon.leagueoflegends.com/cdn/10.22.1/img/item/{item_id}.png'
    html = HTML(f'<img src="{image_url}"/>')
    display(html)

def display_champion(champion_name):
    image_url = f'http://ddragon.leagueoflegends.com/cdn/10.22.1/img/champion/{champion_name}.png'
    html = HTML(f'<img src="{image_url}"/>')
    display(html)
