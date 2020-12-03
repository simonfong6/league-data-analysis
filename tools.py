"""
Various tools and functions to operate on the data which is reusable.
"""
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

