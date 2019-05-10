#!/bin/env python3

import copy
import json

ATT = 'ATT'
MID = 'MID'
DEF = 'DEF'
SUB = 'SUB'

REQUIRED_QTR_COUNT = 3

FIELD = {
    ATT: {'max_players': 6, 'assigned_players': []},
    DEF: {'max_players': 4, 'assigned_players': []},
    SUB: {'max_players': -1, 'assigned_players': []}
    }
PLAYERS = {
    'AM': {'name': 'AM', 'position': ATT, 'total_qtrs': 5, 'subbed': False}
    , 'AP': {'name': 'AP', 'position': DEF, 'total_qtrs': 25, 'subbed': False}
    , 'BL': {'name': 'BL', 'position': DEF, 'total_qtrs': 10, 'subbed': False}
    , 'E': {'name': 'E', 'position': DEF, 'total_qtrs': 12, 'subbed': False}
    , 'H': {'name': 'H', 'position': ATT, 'total_qtrs': 19, 'subbed': False}
    , 'JC': {'name': 'JC', 'position': DEF, 'total_qtrs': 20, 'subbed': False}
    , 'JJ': {'name': 'JJ', 'position': ATT, 'total_qtrs': 21, 'subbed': False}
    , 'LC': {'name': 'LC', 'position': ATT, 'total_qtrs': 9, 'subbed': False}
    , 'LP': {'name': 'LP', 'position': DEF, 'total_qtrs': 18, 'subbed': False}
    , 'M': {'name': 'M', 'position': ATT, 'total_qtrs': 23, 'subbed': False}
    , 'NA': {'name': 'NA', 'position': DEF, 'total_qtrs': 25, 'subbed': False}
    , 'NB': {'name': 'NB', 'position': DEF, 'total_qtrs': 25, 'subbed': False}
    , 'ND': {'name': 'ND', 'position': ATT, 'total_qtrs': 20, 'subbed': False}
}


def game_assigner():
    # Q1 Assign players based on preference, put left overs in subs.
    # Q2-Q4 Take subs and replace players on field that haven't subbed.
    _reset_players()
    qtr_count = 1
    game = []
    current_quarter = quarter_assigner(copy.deepcopy(FIELD))
    game.append(copy.deepcopy(current_quarter))
    while qtr_count < 4:
        current_quarter = quarter_assigner(current_quarter)
        qtr_count += 1
        game.append(copy.deepcopy(current_quarter))
    return game


def quarter_assigner(current_quarter):
    if not current_quarter[SUB]['assigned_players']:
        return _first_quarter(current_quarter)
    # Take subs and place into positions
    new_subs = []
    for player in current_quarter[SUB]['assigned_players']:
        position = player['position']
        new_sub_list = [
            plyr for plyr in
            current_quarter[position]['assigned_players']
            if not plyr['subbed']
        ]
        if not new_sub_list:
            position = ATT if position == DEF else DEF
            new_sub_list = [
                plyr for plyr in
                current_quarter[position]['assigned_players']
                if not plyr['subbed']
            ]
        new_sub = new_sub_list.pop()
        current_quarter[position]['assigned_players'].remove(new_sub)
        current_quarter[position]['assigned_players'].append(player)
        player['game_qtrs'] += 1
        player['total_qtrs'] += 1
        new_sub['subbed'] = True
        new_subs.append(new_sub)
    current_quarter[SUB]['assigned_players'] = new_subs
    return current_quarter


def _first_quarter(current_quarter):
    for position in current_quarter:
        potential_players = [
            player for player in sorted(
                PLAYERS,
                key=lambda x: (
                    PLAYERS[x]['game_qtrs'],
                    PLAYERS[x]['total_qtrs']
                ),
                reverse=True
            )
            if PLAYERS[player]['position'] == position
            and PLAYERS[player] not in
            current_quarter[position]['assigned_players']
        ]
        if not current_quarter[position]['max_players'] and position != SUB:
            selected_player = _get_viable_player(potential_players)
            current_quarter[position]['assigned_players'].append(
                selected_player
            )
            selected_player['total_qtrs'] += 1
            selected_player['game_qtrs'] += 1
        while len(current_quarter[position]['assigned_players']) \
                < current_quarter[position]['max_players']:
            selected_player = _get_viable_player(potential_players)
            current_quarter[position]['assigned_players'].append(
                selected_player
            )
            selected_player['total_qtrs'] += 1
            selected_player['game_qtrs'] += 1

    current_quarter[SUB]['assigned_players'] = [
        PLAYERS[player] for player in PLAYERS
        if PLAYERS[player] not in current_quarter[ATT]['assigned_players']
        and PLAYERS[player] not in current_quarter[DEF]['assigned_players']
    ]
    for player in current_quarter[SUB]['assigned_players']:
        player['subbed'] = True
    return current_quarter


def _get_viable_player(potential_players):
    return PLAYERS[potential_players.pop()]


def _reset_players():
    for player in PLAYERS:
        PLAYERS[player]['game_qtrs'] = 0


if  __name__ == '__main__':
    import json
    print(json.dumps(game_assigner(PLAYERS, FIELD), indent=2))
