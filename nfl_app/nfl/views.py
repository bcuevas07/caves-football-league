import json

from datetime import date, time
from django.http import JsonResponse
from django.shortcuts import render

from nfl.deorators import post_only
from nfl.utils import get_current_games, get_games_by_week, get_team_records, get_participant_records, get_byes_by_week, \
    get_current_week, PENTHOUSE, RANKING_LIST


# Create your views here.


def home(request):
    participant_scores = get_participant_records()
    # the current implementation expects each participant to have 4 teams, so the template that loads this data
    # will only display team_1 through team_4 for each participant. We can make this more flexible if desired.

    standings = {}
    count = 0
    location = PENTHOUSE
    wins = -1
    for participant in sorted(participant_scores, key=lambda k: k['wins'], reverse=True):
        if location not in standings.keys():
            # new location, so participant automatically gets entered at the location
            standings[location] = {'location': RANKING_LIST[location], 'name': [participant['name']]}
            wins = participant['wins']
            count += 1
        else:
            # location already created, so check if participant is tied or has less wins
            if participant['wins'] == wins:
                # tied, so share the same location
                standings[location]['name'].append(participant['name'])
                count += 1
            else:
                # participant has less wins, so automatically gets put in next location
                wins = participant['wins']
                standings[location]['name'] = ', '.join(standings[location]['name']) # convert list to a comma separated string
                location = PENTHOUSE - count
                standings[location] = {'location': RANKING_LIST[location], 'name': [participant['name']]}
                count += 1

    # check if the last processed location added needs to convert the list of names to a comma separated string
    if isinstance(standings[location]['name'], list):
        standings[location]['name'] = ', '.join(standings[location]['name'])

    # reverse the list since it puts the outhouse (0) on top, but we want the penthouse (7) on top
    standings_list = list(standings.values())
    standings_list.reverse()
    return render(request, 'home.html', context={'part_scores': participant_scores, 'standings': standings_list})


def current_week(request):
    games = get_current_games()
    current_week = get_current_week()
    byes = get_byes_by_week(current_week, json_format=True)
    return render(request, 'current_week.html', context={'games': games, 'byes': byes, 'week': current_week})


def season_scores(request):
    team_scores = get_team_records()
    afc_north = []
    afc_east = []
    afc_south = []
    afc_west = []
    nfc_north = []
    nfc_east = []
    nfc_south = []
    nfc_west = []
    for team in team_scores.keys():
        if team_scores[team]['division'].lower() == 'north':
            if team_scores[team]['conference'].lower() == 'afc':
                afc_north.append(team_scores[team])
            else:
                nfc_north.append(team_scores[team])
        elif team_scores[team]['division'].lower() == 'east':
            if team_scores[team]['conference'].lower() == 'afc':
                afc_east.append(team_scores[team])
            else:
                nfc_east.append(team_scores[team])
        elif team_scores[team]['division'].lower() == 'south':
            if team_scores[team]['conference'].lower() == 'afc':
                afc_south.append(team_scores[team])
            else:
                nfc_south.append(team_scores[team])
        elif team_scores[team]['division'].lower() == 'west':
            if team_scores[team]['conference'].lower() == 'afc':
                afc_west.append(team_scores[team])
            else:
                nfc_west.append(team_scores[team])
    return render(request, 'season_scores.html',
                  context={'afc_north': afc_north, 'afc_east': afc_east, 'afc_south': afc_south, 'afc_west': afc_west,
                           'nfc_north': nfc_north, 'nfc_east': nfc_east, 'nfc_south': nfc_south, 'nfc_west': nfc_west})


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
