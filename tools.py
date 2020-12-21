"""
Various tools and functions to operate on the data which is reusable.
"""
import json
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from league_api import *


DATA_DIRECTORY = './data'


def data_path(path):
    full_path = os.path.join(DATA_DIRECTORY, path)
    return full_path


def list_data_files():
    data_files = os.listdir(DATA_DIRECTORY)
    data_files.sort()
    return data_files


def load(name):
    path = data_path(name)
    df = pd.read_pickle(path)
    return df


def create_subset(name, size):
    df = load(name)
    subset = df[:size]

    subset_name, _ = name.split('.')
    subset_path = f'data/{subset_name}_subset_{size}.pickle'
    subset.to_pickle(subset_path)

    print(f'Saved to {subset_path}')


def display_dict(dict_obj):
    string = json.dumps(dict_obj, indent=4)
    print(string)


def create_example_participant():
    match_df = load('match_data_version1_subset_1000.pickle')
    participants = match_df['participants']
    participant = participants[0][0]
    with open('data/example_participant.json', 'w') as f:
        json.dump(participants[0][0], f, indent=4)

def filter_participant(participant):
    keys = [
        'participantId',
        'teamId',
        'championId',
    ]

    stats_keys = [
        'win',
        'item0',
        'item1',
        'item2',
        'item3',
        'item4',
        'item5',
        'item6',
        'kills',
        'deaths',
        'assists',
    ]

    timeline_keys = [
        'role',
        'lane',
    ]

    filtered = {}
    for key in keys:
        filtered[key] = participant[key]

    for key in stats_keys:
        filtered[key] = participant['stats'][key]
        
    for key in timeline_keys:
        filtered[key] = participant['timeline'][key]
    
    return filtered


def champion_name_to_champion_id(champion_name):
    champion_id = None

    return champion_id


def winrate(current_champion, opponent_champion, item, dataset=None):
    # Filter for matches with current and opponent_champion
    # Filter for item
    return 0.5


def has_champion_id(participants, champion_id):
    participant_champion_id_matches = lambda participant: str(participant['championId']) == str(champion_id)

    matches = map(participant_champion_id_matches, participants)
    
    has_a_single_match = any(matches)
    
    return has_a_single_match


def create_has_champion_id_func(champion_id):
    return lambda participants: has_champion_id(participants, champion_id)


def create_champion_on_lane(champion_id, lane):

    def champion_on_lane(participants):
        # Filter for champion.
        matches_champion_func = lambda participant: participant['championId'] == champion_id
        matches_champion = filter(matches_champion_func, participants)
        matches_champion = list(matches_champion)
        participant, = matches_champion

        # Check if lane matches.
        return participant['timeline']['lane'] == lane

    return champion_on_lane


def filter_matching_lanes(current_champion_id, opponent_champion_id, lane, matches):
    participants = matches['participants']

    filtered = participants

    # Filter for has current champion.
    has_current_champion = create_has_champion_id_func(current_champion_id)
    conditions = filtered.apply(has_current_champion)
    filtered =  filtered[conditions]

    # Filter for has opponent champion.
    has_opponent_champion = create_has_champion_id_func(opponent_champion_id)
    conditions = filtered.apply(has_opponent_champion)
    filtered =  filtered[conditions]

    # Filter current champion on lane.
    current_champion_on_lane = create_champion_on_lane(current_champion_id, lane)
    conditions = filtered.apply(current_champion_on_lane)
    filtered =  filtered[conditions]

    # Filter opponent champion on lane.
    opponent_champion_on_lane = create_champion_on_lane(opponent_champion_id, lane)
    conditions = filtered.apply(opponent_champion_on_lane)
    filtered =  filtered[conditions]
    
    return filtered

def reduce_participants(participants_series, champion_id):
    def find_champion(participants):
        for participant in participants:
            if participant['championId'] == champion_id:
                return participant
        raise ValueError("Not found.")

    reduced = participants_series.apply(find_champion)

    return reduced

def filter_participant_series_keys(participants_series):
    filtered = participants_series.apply(filter_participant)
    return filtered


def display_participant(participant):
    champion_id_to_champion = create_champion_dict()
    item_map = create_item_map()

    champion_id = participant['championId']
    champion_name = champion_id_to_champion[champion_id]['id']
    print(champion_name)
    display_champion(champion_name)

    for key, value in participant.items():
        if key in set(['lane', 'win']):
            print(f"{key.capitalize()}: {value}")

    for key, value in participant.items():
        if 'item' not in key:
            continue

        # No item in spot.
        if value == 0:
            continue
        item_id = str(value)
        item_name = item_map[item_id]['name']
        print(item_id)
        print(item_name)
        display_item(item_id)


def convert_item_id_to_name(item_id):
    item_map = create_item_map()
    item_id = str(item_id)
    item_name = item_map[item_id]['name']

    return item_name


def display_item_with_winrate(item_id, win_rate, uses):
    item_id = int(item_id)
    item_name = convert_item_id_to_name(item_id)
    display_item(item_id)
    percent = f"Win Rate: {win_rate:.0%}"
    uses_string = f"Uses: {uses}"
    print(item_name)
    print(percent)
    print(uses_string)


def display_items_by_winrate(participant_series):
    from collections import Counter

    ITEM_KEYS = list(map(lambda num: f"item{num}", range(7)))

    item_wins = Counter()
    item_used = Counter()

    for participant in participant_series:
        win = participant['win']
        for item_key in ITEM_KEYS:
            item_id = participant[item_key]
            
            # Skip empty item slots
            if item_id == 0:
                continue

            item_used[item_id] += 1
            
            if win:
                item_wins[item_id] += 1

    # Calculate win rates.
    item_win_rates = Counter()
    for item_id, item_uses in item_used.items():
        wins = item_wins[item_id]
        win_rate = wins / item_uses
        
        item_win_rates[item_id] = win_rate

    # Sort by highest win rate and display.
    for item_id, win_rate in item_win_rates.most_common():
        uses = item_used[item_id]
        display_item_with_winrate(item_id, win_rate, uses)
