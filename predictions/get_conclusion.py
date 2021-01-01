# Algortihm to predict the winner:

# 1) By experts for W1 and W2
# 2) By past matches' resutls (relevant past matches)
# 3) By stats collected from tennislive and ultimate_stats
# 4) By tennis predictor websites (percentage showing websites)
# 5) By odds
# 6) By various stats show on ultimate_stats (like mentality)
# 7) Past results between players
# 8) By playing at home
# 9) By age (if very young or very old - a big minus)
# 10) By experience (non-experienced player against experienced player)
# 11) Consider expert's stats (current profit %)
# 12) Prize pool/Prestigeness of the tournament (motivation to win it).
# E.g., for top players - low motivation to play atp 250, challengers etc, for low players - vice versa
# 13)


import math
import random
import matplotlib
import numpy as np


def get_points(past_results, winner_odds, winner_picks_ration, **kwargs):
    points = int()
    # name, past_results, winner_odss, winner_picks, rank, rank_peak, atp_points, age, money_won, total_mathces, winrate
    # TODO: CHECK IF ALL SOME KWARGS ARE NOT `None`

    return points


# def get_conclusion(player1_data: dict, player2_data: dict):
def get_conclusion(*args, **kwargs):
    # Based on points
    conclusion = None
    return conclusion


# Constant rates
betSTATS = {'Odds': -100, 'BetsTendency': 0.1,
            'PastResults': 20, 'Predictions': None, }
ovarallSTATS = {'Age': {'>33': -20, '<20': -15},
                'Ranking': 'Reversed * 1000',
                'RankingPeak': 'Reverded * 500', 'Points': 0.1,
                'PrizeMoney': 'Who has more +',
                'TotalMathces': 0.1, 'Winrate%': 'Who has more +'}
gameSTATS = {'Ace %': 'Ace'*10, 'Double Fault %': 'Fault'*-10,
             '1st Serve %': {'>55': 100, '<50': -100},
             '1st Serve Won %': {'>67': 100, '<50': -100},
             '2nd Serve Won %': {'>50': 100, '<43': -100},
             'Titles': 'Title'*10, 'GOAT Rank': 'Reversed'*500}


PREVIOUS_MATCH = 20
ODDS = -100
OLD = -30
YOUNG = -15
PEAK_AGE = 20
RANK_PTS = 0.01
PRIZE = 0.000001
MATCHES = 0.1
HIGH_WINRATE = 300
MID_WINRATE = (-100, 100)   # random integer
LOW_WINRATE = -300
ACE = 50
FAULT = -40
FIRST_SERVE  =



def get_outcome(players_stats: dict, betting_stats: dict, h2h: dict):
    points = {}

    for player, stats in players_stats.items():
        pts = int()

        odds = betting_stats['Odds'][player]
        n_times_picked = betting_stats['BetsTendency'][player]
        past_matches = betting_stats['PastResults'][player]

        # +- 20 * `i` for each won or lost past match amongst 5 last matches
        # Where `i` is a relevancy factor, e.g., a win 3 days ago will be weightier that a win 10 days ago
        if past_matches:
            for i, match in enumerate(past_matches):
                if match == '+':
                    pts += 1 / i * PREVIOUS_MATCH
                else:
                    pts += 1 / i * (-PREVIOUS_MATCH)

        if n_times_picked:
            pts += n_times_picked * 0.1

        age = stats.get('Age')
        if age:
            # Too old -> minus
            if age >= 33:
                pts += OLD
            # Too young -> minus
            elif age <= 19:
                pts += YOUNG
            # Peak age -> plus
            elif age <= 26 and age >= 22:
                pts += PEAK_AGE
            # Other ages do not affect
            else:
                pass
        
        rank = stats.get('Ranking')
        if rank:
            # Higher (gravitating -> 1) the plus is bigger (inverse proportion)
            pts += 1 / rank * 500

        rank_peak = stats.get('RankingPeak')
        if rank_peak:
            # Almost the same here but plus is slightly less
            pts += 1 / rank_peak * 250

        # rank_pts = stats.get('Points')
        # if rank_pts:
        #     # More ATP/WTA points -> plus
        #     pts += rank_pts * RANK_PTS

        prize = stats.get('PrizeMoney')
        if prize:
            # More prize money -> plus
            pts += prize * PRIZE

        matches = stats.get('TotalMatches')
        if matches:
            pts += matches * MATCHES

        winrate = stats.get('Winrate')
        if winrate:
            if winrate >= 62:
                winrate += HIGH_WINRATE
            elif winrate <= 45:
                winrate -= LOW_WINRATE
            else:
                winrate += random.randint(*MID_WINRATE)
        
        ace = stats.get('Ace %')
        if ace:
            pts += ace * ACE 

        fault = stats.get('Fault %')
        if fault:
            pts += fault * FAULT
                
        first_serve = stats.get('1st Serve %')
        if first_serve:
            pts += first_server * FIRST_SERVE

        # In the end reduce points considering odds ratio
        if odds:
            pts += ODDS * odds


        points[player] = pts

    outcome = str()
    return outcome


if __name__ == '__main__':
    pass
