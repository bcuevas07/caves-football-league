import json

from datetime import date, time
from django.http import JsonResponse
from django.shortcuts import render

from nfl.deorators import post_only
from nfl.utils import get_current_games, get_games_by_week, get_team_records, get_participant_records


# Create your views here.


def home(request):
    participant_scores = get_participant_records()
    return render(request, 'home.html', context={'part_scores': participant_scores})


def current_week(request):
    games = get_current_games()
    return render(request, 'current_week.html', context={'games': games})


def season_scores(request):
    team_scores = get_team_records()
    teams = []
    for team in team_scores.keys():
        teams.append(team_scores[team])
    return render(request, 'season_scores.html', context={'team_scores': teams})


def weekly_schedule(request):
    games = []
    return render(request, 'weekly_schedule.html', context={'games': games})


@post_only
def ajax_week_schedule(request, week):
    # week = request.POST.get('week', -1)

    games = get_games_by_week(week, json_format=True)
    json_games = json.dumps(games, default=_serialize)
    return JsonResponse(json_games, safe=False)


def _serialize(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, date):
        serial = obj.isoformat()
        return serial

    if isinstance(obj, time):
        serial = obj.isoformat()
        return serial
    return obj.__dict__
