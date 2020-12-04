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
