from datetime import datetime

import numpy as np
import pandas as pd

from core.models import Match, Group

# todo: creo que esto habria que completarlo...
BATACAZOS = {
    '2': 'Uruguay'
}


def obtain_group_zone_games():
    groups_info = pd.read_csv('calculator/data/group_zone_matches.csv')
    for index, row in groups_info.iterrows():
        group = Group.get_or_create(group_name=row['group'])
        date = datetime.strptime(row['date'], '%d/%m/%Y %H:%M')
        Match.new_with(date=date, home_team=row['home'], visiting_team=row['visiting'], group=group)


def obtain_results():
    results = pd.read_csv('calculator/data/results.csv', index_col=['match_id'])
    return results


def calculate_score(predictions):
    total_score = 0
    results = obtain_results()

    for prediction in predictions:
        match_score = 0

        match_id = prediction.match().id
        try:
            match_info = results.loc[match_id]
        except KeyError:
            continue

        if not hit_the_winning_team(prediction, match_info['winning_team']):
            continue

        match_score += 10
        if hit_distance_between_teams(prediction, match_info) and not prediction.is_draw():
            match_score += 5

        if hit_goals_of_both_teams(prediction, match_info):
            match_score += 2

        if result_is_unexpected(prediction):
            match_score *= 2

        total_score += match_score

    return total_score


def hit_the_winning_team(prediction, winning_team):
    if prediction.is_draw() and winning_team != 0:
        return False
    elif prediction.winning_team() != winning_team:
        return False
    else:
        return True


def hit_distance_between_teams(prediction, match_info):
    predicted_distance = np.linalg.norm(prediction.home_team_goals() - prediction.visiting_team_goals())
    real_distance = np.linalg.norm(match_info['home_team_goals'] - match_info['visiting_team_goals'])

    return predicted_distance == real_distance


def hit_goals_of_both_teams(prediction, match_info):
    return prediction.home_team_goals() == match_info['home_team_goals'] and \
           prediction.visiting_team_goals() == match_info['visiting_team_goals']


def result_is_unexpected(prediction):
    match_id = prediction.match().id

    if match_id not in BATACAZOS:
        return False

    return prediction.winning_team() == BATACAZOS[match_id]
