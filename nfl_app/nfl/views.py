import json

from datetime import date, time
from django.http import JsonResponse
from django.shortcuts import render

from nfl.deorators import post_only
from nfl.utils import get_current_games, get_games_by_week, get_team_records, get_participant_records, get_byes_by_week, \
    get_current_week


# Create your views here.


def home(request):
    participant_scores = get_participant_records()
    # the current implementation expects each participant to have 4 teams, so the template that loads this data
    # will only display team_1 through team_4 for each participant. We can make this more flexible if desired.
    return render(request, 'home.html', context={'part_scores': participant_scores})


def current_week(request):
    games = get_current_games()
    current_week = get_current_week()
    byes = get_byes_by_week(current_week, json_format=True)
    return render(request, 'current_week.html', context={'games': games, 'byes': byes, 'week': current_week})


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
    result = {'games': games, 'bye_week': get_byes_by_week(week, json_format=False)}
    json_result = json.dumps(result, default=_serialize)
    return JsonResponse(json_result, safe=False)


def _serialize(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, date):
        serial = obj.isoformat()
        return serial

    if isinstance(obj, time):
        serial = obj.isoformat()
        return serial
    return obj.__dict__
