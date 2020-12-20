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


def filter_matching_lanes(current_champion, opponent_champion, matches):
    participants = matches['participants']
    filtered = []
    
    return filtered
