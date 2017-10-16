from django.shortcuts import render
from nfl.utils import get_current_games
from nfl.nfl_game import NflGame
from datetime import datetime
# Create your views here.


def home(request):
    return render(request, 'home.html')


def current_week(request):
    games = get_current_games()
    games.append(NflGame({
            "gsisId": "2017100900",
            "seasonYear": 2017,
            "startTime": "20171010T003000.000Z",
            "timeInserted": "20170803T145501.334Z",
            "dayOfWeek": "Monday",
            "gameKey": "57311",
            "finished": True,
            "homeTeam": {
                "scoreQ3": 7,
                "turnovers": 0,
                "scoreQ2": 0,
                "score": 17,
                "team": "CHI",
                "scoreQ1": 2,
                "scoreQ4": 8
            },
            "timeUpdate": "20171010T115412.165Z",
            "awayTeam": {
                "scoreQ3": 14,
                "turnovers": 1,
                "scoreQ2": 3,
                "score": 20,
                "team": "MIN",
                "scoreQ1": 0,
                "scoreQ4": 3
            },
            "week": "NflWeek5",
            "seasonType": "Regular"
        }))
    return render(request, 'current_week.html', context={'games': games})