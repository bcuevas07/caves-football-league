import json

import os
import requests

from config.settings.base import BASE_DIR, OFFLINE_MODE
from .nfl_game import NflGame, SEASON_GAME_TYPE

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

TEAM_ID_MAP = {
    'Arizona Cardinals': 'ARI',
    'Atlanta Falcons': 'ATL',
    'Baltimore Ravens': 'BAL',
    'Buffalo Bills': 'BUF',
    'Carolina Panthers': 'CAR',
    'Chicago Bears': 'CHI',
    'Cincinnati Bengals': 'CIN',
    'Cleveland Browns': 'CLE',
    'Dallas Cowboys': 'DAL',
    'Denver Broncos': 'DEN',
    'Detroit Lions': 'DET',
    'Green Bay Packers': 'GB',
    'Houston Texans': 'HOU',
    'Indianapolis Colts': 'IND',
    'Jacksonville Jaguars': 'JAC',
    'Kansas City Chiefs': 'KC',
    'Los Angeles Chargers': 'LAC',
    'Los Angeles Rams': 'LA',
    'Miami Dolphins': 'MIA',
    'Minnesota Vikings': 'MIN',
    'New England Patriots': 'NE',
    'New Orleans Saints': 'NO',
    'New York Giants': 'NYG',
    'New York Jets': 'NYJ',
    'Oakland Raiders': 'OAK',
    'Philadelphia Eagles': 'PHI',
    'Pittsburgh Steelers': 'PIT',
    'Seattle Seahawks': 'SEA',
    'San Francisco 49ers': 'SF',
    'Tampa Bay Buccaneers': 'TB',
    'Tennessee Titans': 'TEN',
    'Washington Redskins': 'WAS'
}

PARTICIPANT_TEAMS = {
    'Bryan': ['Atlanta Falcons', 'Tampa Bay Buccaneers', 'Indianapolis Colts', 'Miami Dolphins'],
    'Daniel': ['New England Patriots', 'Carolina Panthers', 'Minnesota Vikings', 'Chicago Bears'],
    'Dorothy': ['Pittsburgh Steelers', 'Kansas City Chiefs', 'Washington Redskins', 'Cincinnati Bengals'],
    'Gabri': ['Green Bay Packers', 'Tennessee Titans', 'Detroit Lions', 'Jacksonville Jaguars'],
    'Martin': ['Los Angeles Chargers', 'New Orleans Saints', 'Los Angeles Rams', 'New York Jets'],
    'Meg': ['Dallas Cowboys', 'Denver Broncos', 'Baltimore Ravens', 'San Francisco 49ers'],
    'Paula': ['Seattle Seahawks', 'Houston Texans', 'Philadelphia Eagles', 'Buffalo Bills'],
    'Vic': ['Oakland Raiders', 'Arizona Cardinals', 'New York Giants', 'Cleveland Browns']
}

PRESEASON_TAG = 'NflPreSeasonWeek'
SEASON_TAG = 'NflWeek'


def get_byes(game_data, json_format=False):
    team_list = []
    bye_list = []
    for game in game_data:
        nfl_game = NflGame(game, json_format=json_format)
        if nfl_game.away_team not in team_list:
            team_list.append(nfl_game.away_team)
        if nfl_game.home_team not in team_list:
            team_list.append(nfl_game.home_team)
    for key in TEAM_ID_MAP.keys():
        if key not in team_list:
            bye_list.append(key)
    return bye_list


def get_byes_by_week(week_data, json_format=False):
    try:
        week = int(week_data)
    except:
        return []
    if week < 1 or week > 17:
        return []
    if OFFLINE_MODE:
        with open(os.path.join(BASE_DIR, 'nfl', 'test_scripts', 'weeks', 'games_2017_{}.json'.format(week))) as file:
            game_data = json.loads(file.read())
    else:
        game_data = _query_database('games/2017/{}'.format(week))
    return get_byes(game_data, json_format=json_format)


def get_current_status():
    """
        json object looks like:
          "seasonYear": 2017,
          "lastRosterDownload": "20171110T132121.435Z",
          "week": "NflWeek10",
          "version": "8",
          "seasonType": "Regular"
    """
    if OFFLINE_MODE:
        with open(os.path.join(BASE_DIR, 'nfl','test_scripts', 'info.json')) as json_file:
            data = json.loads(json_file.read())
    else:
        data = _query_database('info')
    return data


def get_current_games():
    game_list = []
    if OFFLINE_MODE:
        with open(os.path.join(BASE_DIR, 'nfl','test_scripts', 'weeks', 'games_2017_10.json')) as json_file:
            game_data = json.loads(json_file.read())
    else:
        game_data = _query_database('games')
    for game in game_data:
        nfl_game = NflGame(game)
        game_list.append(nfl_game)
    return game_list


def get_current_week():
    info = get_current_status()
    week = -1
    if info and 'week' in info.keys():
        week_str = info['week'].replace(PRESEASON_TAG, '').replace(SEASON_TAG, '')
        try:
            week = int(week_str)
        except:
            print('Error parsing current week text. String is not a valid integer: {}'.format(week_str))
    return week


def get_games_by_week(data, json_format=False):
    try:
        week = int(data)
    except:
        return []
    if week < 1 or week > 17:
        return []
    game_list = []
    if OFFLINE_MODE:
        with open(os.path.join(BASE_DIR, 'nfl', 'test_scripts', 'weeks', 'games_2017_{}.json'.format(week))) as file:
            game_data = json.loads(file.read())
    else:
        game_data = _query_database('games/2017/{}'.format(week))
    for game in game_data:
        game_list.append(NflGame(game, json_format=json_format))
    return game_list


def get_games_by_year(year):
    game_list = []
    if OFFLINE_MODE:
        with open(os.path.join(BASE_DIR, 'nfl' ,'test_scripts', 'year', '{}.json'.format(year))) as json_file:
            game_data = json.loads(json_file.read())
    else:
        game_data = _query_database('games/{}'.format(year))
    for game in game_data:
        nfl_game = NflGame(game)
        game_list.append(nfl_game)
    return game_list


def get_participant_records():
    team_scores = get_team_records()
    participant_scores = []
    if team_scores and len(team_scores) > 0:
        for participant in PARTICIPANT_TEAMS.keys():
            individual_score = {'name': participant, 'wins': 0}
            for team in PARTICIPANT_TEAMS[participant]:
                individual_score['wins'] += team_scores[team]['wins']
            participant_scores.append(individual_score)
    return participant_scores

def get_team_records():
    team_scores = {}
    games = get_games_by_year(2017)
    for game in games:
        if game.finished and game.season_type == SEASON_GAME_TYPE and (game.home_score > 0 or game.away_score > 0):
            if game.home_team not in team_scores.keys():
                team_scores[game.home_team] = {'wins': 0, 'losses': 0, 'ties': 0, 'name': game.home_team,
                                               'conference': TEAM_DETAILS[TEAM_ID_MAP[game.home_team]]['conference'],
                                               'division': TEAM_DETAILS[TEAM_ID_MAP[game.home_team]]['division'].upper()}
            if game.away_team not in team_scores.keys():
                team_scores[game.away_team] = {'wins': 0, 'losses': 0, 'ties': 0, 'name': game.away_team,
                                               'conference': TEAM_DETAILS[TEAM_ID_MAP[game.away_team]]['conference'],
                                               'division': TEAM_DETAILS[TEAM_ID_MAP[game.away_team]]['division'].upper()}

            if game.home_score > game.away_score:
                team_scores[game.home_team]['wins'] += 1
                team_scores[game.away_team]['losses'] += 1
            elif game.away_score > game.home_score:
                team_scores[game.away_team]['wins'] += 1
                team_scores[game.home_team]['losses'] += 1
            else: #tie
                team_scores[game.home_team]['ties'] += 1
                team_scores[game.away_team]['ties'] += 1
    return team_scores


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
