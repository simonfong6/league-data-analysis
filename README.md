# league-data-analysis
League Data Analysis

# Data
- The data is very large and cannot be stored in version control.
- Everytime we operate on it, we must download the zip, and unzip it into the
data directory.
- [data](https://www.kaggle.com/gyejr95/league-of-legendslol-ranked-games-2020-ver1)
- Directory should look like:
```
league-data-analysis/data/
    archive.zip
    challenger_match_V2.csv
    ...
    match_winner_data_version1.csv
    match_winner_data_version1.pickle
```

# Plan
- Shared helper functions in `tools.py` and various other files we create.
- We each use our own notebooks to do analysis. (Easier for version control.)
