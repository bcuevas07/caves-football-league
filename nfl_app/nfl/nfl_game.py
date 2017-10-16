import datetime


class NflGame():
    def __init__(self, game_data):
        # {
        #     "gsisId": "2017100900",
        #     "seasonYear": 2017,
        #     "startTime": "20171010T003000.000Z",
        #     "timeInserted": "20170803T145501.334Z",
        #     "dayOfWeek": "Monday",
        #     "gameKey": "57311",
        #     "finished": true,
        #     "homeTeam": {
        #         "scoreQ3": 7,
        #         "turnovers": 0,
        #         "scoreQ2": 0,
        #         "score": 17,
        #         "team": "CHI",
        #         "scoreQ1": 2,
        #         "scoreQ4": 8
        #     },
        #     "timeUpdate": "20171010T115412.165Z",
        #     "awayTeam": {
        #         "scoreQ3": 14,
        #         "turnovers": 1,
        #         "scoreQ2": 3,
        #         "score": 20,
        #         "team": "MIN",
        #         "scoreQ1": 0,
        #         "scoreQ4": 3
        #     },
        #     "week": "NflWeek5",
        #     "seasonType": "Regular"
        # }
        from nfl.utils import TEAM_DETAILS # Cannot import this on start-up since utils loads this file

        self.id = game_data['gsisId']
        self.year = game_data['seasonYear']
        self.start_time = datetime.datetime.strptime(game_data['startTime'].split('.')[0], '%Y%m%dT%H%M%S')
        self.day = game_data['dayOfWeek']
        self.week = game_data['week'][7:] # First seven characters are always NflWeek
        self.season_type = game_data['seasonType'].lower()
        self.finished = game_data['finished']
        self.home_team = TEAM_DETAILS[game_data['homeTeam']['team']]['name']
        self.away_team = TEAM_DETAILS[game_data['awayTeam']['team']]['name']
        self.home_score = game_data['homeTeam']['score']
        self.away_score = game_data['awayTeam']['score']

    def get_result(self):
        return '{} - {}'.format(self.away_score, self.home_score)

    def __str__(self):
        return '{} @ {}'.format(self.away_team, self.home_team)
