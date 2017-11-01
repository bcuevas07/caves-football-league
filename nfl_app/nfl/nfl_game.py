import datetime
from pytz import timezone

SEASON_GAME_TYPE = 'regular'
PRESEASON_GAME_TYPE = 'preseason'

class NflGame():
    def __init__(self, game_data, json_format=False):
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
        # self.start_time = datetime.datetime.strptime(game_data['startTime'].split('.')[0], '%Y%m%dT%H%M%S')
        self.start_time = datetime.datetime.strptime(game_data['startTime'], '%Y%m%dT%H%M%S.%fZ')
        self.start_time = timezone('UTC').localize(self.start_time)
        if json_format:
            self.start_time = self._json_format_datetime(self.start_time)
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

    def _json_format_datetime(self, obj):
        obj = obj.astimezone(timezone('US/Pacific'))
        day = obj.strftime('%A')
        date = obj.strftime('%m/%d/%Y')
        time = obj.strftime('%I:%M %p').lower()
        result = '{} {} @ {}'.format(day, date, time)
        return result

    def is_team_win(self, team_id):
        """
            Determines if the team_id won or lost the game.
        :param team_id:
        :return:
                True if team_id won
                False if team_id lost
                None if team_id is not part of this game
        """
        if self.home_team == team_id:
            return self.home_score > self.away_score
        elif self.away_team == team_id:
            return self.away_score > self.home_score
        else:
            return None
