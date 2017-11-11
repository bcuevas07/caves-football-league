from nfl.utils import _query_database, TEAM_DETAILS

def generate_weeks():
    for index in range(1, 18):
        with open('test_scripts/weeks/games_2017_{}.json'.format(index), 'w') as json_file:
            json_file.write(str(_query_database('games/2017/{}'.format(index))).replace('True', 'true')
                            .replace('False', 'false').replace("'", '"'))

def generate_team_data():
    for key in TEAM_DETAILS.keys():
        with open('test_scripts/teams/{}.json'.format(key), 'w') as json_file:
            json_file.write(str(_query_database('team/{}/schedule'.format(key))).replace('True', 'true')
                            .replace('False', 'false').replace("'", '"'))


def generate_year_data():
        for index in range(2009, 2018):
            with open('test_scripts/year/{}.json'.format(index), 'w') as json_file:
                json_file.write(str(_query_database('games/{}'.format(index))).replace('True', 'true')
                                .replace('False', 'false').replace("'", '"'))


if __name__ == '__main__':
    generate_weeks()
    generate_team_data()
    generate_year_data()