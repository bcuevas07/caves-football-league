import json

import os
import requests

from config.settings.base import BASE_DIR, OFFLINE_MODE
from .nfl_game import NflGame

TEAM_DETAILS = {
    'ARI': {'name': 'Arizona Cardinals', 'division': 'west', 'conference': 'NFC'},
    'ATL': {'name': 'Atlanta Falcons', 'division': 'south', 'conference': 'NFC'},
    'BAL': {'name': 'Baltimore Ravens', 'division': 'north', 'conference': 'AFC'},
    'BUF': {'name': 'Buffalo Bills', 'division': 'east', 'conference': 'AFC'},
    'CAR': {'name': 'Carolina Panthers', 'division': 'south', 'conference': 'NFC'},
    'CHI': {'name': 'Chicago Bears', 'division': 'north', 'conference': 'NFC'},
    'CIN': {'name': 'Cincinnati Bengals', 'division': 'north', 'conference': 'AFC'},
    'CLE': {'name': 'Cleveland Browns', 'division': 'north', 'conference': 'AFC'},
    'DAL': {'name': 'Dallas Cowboys', 'division': 'east', 'conference': 'NFC'},
    'DEN': {'name': 'Denver Broncos', 'division': 'west', 'conference': 'AFC'},
    'DET': {'name': 'Detroit Lions', 'division': 'north', 'conference': 'NFC'},
    'GB': {'name': 'Green Bay Packers', 'division': 'north', 'conference': 'NFC'},
    'HOU': {'name': 'Houston Texans', 'division': 'south', 'conference': 'AFC'},
    'IND': {'name': 'Indianapolis Colts', 'division': 'south', 'conference': 'AFC'},
    'JAC': {'name': 'Jacksonville Jaguars', 'division': 'south', 'conference': 'AFC'},
    'KC': {'name': 'Kansas City Chiefs', 'division': 'west', 'conference': 'AFC'},
    'LAC': {'name': 'Los Angeles Chargers', 'division': 'west', 'conference': 'AFC'},
    'LA': {'name': 'Los Angeles Rams', 'division': 'west', 'conference': 'NFC'},
    'MIA': {'name': 'Miami Dolphins', 'division': 'east', 'conference': 'AFC'},
    'MIN': {'name': 'Minnesota Vikings', 'division': 'north', 'conference': 'NFC'},
    'NE': {'name': 'New England Patriots', 'division': 'east', 'conference': 'AFC'},
    'NO': {'name': 'New Orleans Saints', 'division': 'south', 'conference': 'NFC'},
    'NYG': {'name': 'New York Giants', 'division': 'east', 'conference': 'NFC'},
    'NYJ': {'name': 'New York Jets', 'division': 'east', 'conference': 'AFC'},
    'OAK': {'name': 'Oakland Raiders', 'division': 'west', 'conference': 'AFC'},
    'PHI': {'name': 'Philadelphia Eagles', 'division': 'east', 'conference': 'NFC'},
    'PIT': {'name': 'Pittsburgh Steelers', 'division': 'north', 'conference': 'AFC'},
    'SEA': {'name': 'Seattle Seahawks', 'division': 'west', 'conference': 'NFC'},
    'SF': {'name': 'San Francisco 49ers', 'division': 'west', 'conference': 'NFC'},
    'TB': {'name': 'Tampa Bay Buccaneers', 'division': 'south', 'conference': 'NFC'},
    'TEN': {'name': 'Tennessee Titans', 'division': 'south', 'conference': 'AFC'},
    'WAS': {'name': 'Washington Redskins', 'division': 'east', 'conference': 'NFC'}
}

def get_current_status():
    data = _query_database('info')
    return data


def get_current_games():
    game_list = []
    game_data = _query_database('games')
    if OFFLINE_MODE:
        with open(os.path.join(BASE_DIR, 'nfl','test_scripts', 'weeks', 'games_2017_7.json')) as json_file:
            game_data = json.loads(json_file.read())
    for game in game_data:
        nfl_game = NflGame(game)
        game_list.append(nfl_game)
    return game_list


def get_games_by_week(data, json_format=False):
    try:
        week = int(data)
    except:
        return []
    if week < 1 or week > 17:
        return []
    game_list = []
    game_data = _query_database('games/2017/{}'.format(week))
    if OFFLINE_MODE:
        with open(os.path.join(BASE_DIR, 'nfl', 'test_scripts', 'weeks', 'games_2017_{}.json'.format(week))) as file:
            game_data = json.loads(file.read())
    for game in game_data:
        game_list.append(NflGame(game, json_format=json_format))
    return game_list


def get_games_by_year(year):
    game_list = []
    game_data = _query_database('games/{}'.format(year))
    for game in game_data:
        nfl_game = NflGame(game)
        game_list.append(nfl_game)
    return game_list


def get_team_schedule(team):
    game_list = []
    if not isinstance(team, str) or team not in TEAM_DETAILS:
        return game_list  # Maybe raise an exception or return some error string instead?
    team_data = _query_database('team/{}/schedule'.format(team))
    for game in team_data:
        nfl_game = NflGame(game)
        game_list.append(nfl_game)
    return game_list


def _query_database(relative_path):
    root_path = 'http://api.suredbits.com/nfl/v0/'
    raw_data = requests.get('{}{}'.format(root_path, relative_path))
    # parsed_data = raw_data.content.decode('UTF-8')
    parsed_data = raw_data.text
    json_data = {}
    from config.settings.base import OFFLINE_MODE
    if raw_data.status_code == 200 and parsed_data is not None and not OFFLINE_MODE: # No internet access or access to the api site
        json_data = json.loads(parsed_data)
    return json_data
