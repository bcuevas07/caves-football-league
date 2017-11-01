import json

from datetime import date, time
from django.http import JsonResponse
from django.shortcuts import render

from nfl.deorators import post_only
from nfl.utils import get_current_games, get_games_by_week
# Create your views here.


def home(request):
    return render(request, 'home.html')


def current_week(request):
    games = get_current_games()
    return render(request, 'current_week.html', context={'games': games})


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