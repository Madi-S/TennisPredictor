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



def get_conclusion(players: list, points: dict):
    # Based on points
    conclusion = None
    return conclusion



PREVIOUS_MATCH = 20
ODDS = -100
OLD = -30
YOUNG = -15
PEAK_AGE = 20
RANK = 500
RANK_PEAK = 250
RANK_PTS = 0.01
PRIZE = 0.000001
MATCHES = 0.1
HIGH_WINRATE = 300
MID_WINRATE = (-100, 100)   # random integer
LOW_WINRATE = -300
ACE = 50
FAULT = -40
HIGH_FIRST_SERVE  = 50
MID_FIRST_SERVE = (-25, 25)
LOW_FIRST_SERVE = -50
FIRST_SERVE_WON = 100
SECOND_SERVE_WON = 150
TITLES = 10
GOAT = 650


def get_outcome(players: list, players_stats: dict, betting_stats: dict, h2h: dict):
    points = dict()
    outcome = str()


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
            if age >= 33:
                pts += OLD
            elif age <= 19:
                pts += YOUNG
            elif age <= 26 and age >= 22:
                pts += PEAK_AGE
            else:
                pass
        
        rank = stats.get('Ranking')
        if rank:
            pts += 1 / rank * RANK

        rank_peak = stats.get('RankingPeak')
        if rank_peak:
            pts += 1 / rank_peak * RANK_PEAK

        rank_pts = stats.get('Points')
        if rank_pts:
            # More ATP/WTA points -> plus
            pts += rank_pts * RANK_PTS

        prize = stats.get('PrizeMoney')
        if prize:
            pts += prize * PRIZE

        matches = stats.get('TotalMatches')
        if matches:
            pts += matches * MATCHES

        winrate = stats.get('Winrate')
        if winrate:
            if winrate >= 62:
                winrate += HIGH_WINRATE
            elif winrate <= 45:
                winrate += LOW_WINRATE
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
            if first_serve >= 63:
                ratio = HIGH_FIRST_SERVE 
            elif first_serve <= 43:
                ratio = LOW_FIRST_SERVE
            else:
                ratio = random.randint(*MID_FIRST_SERVE)

            pts += ratio * first_serve / 100

        first_serve_won = stats.get('1nd Serve Won %')
        if first_serve_won:
            if first_serve_won >= 63:
                pts += FIRST_SERVE_WON * first_serve_won / 100
            elif first_serve_won <= 50:
                pts += -FIRST_SERVE_WON
            else:
                pass
                    
        second_serve_won = stats.get('2nd Serve Won %')
        if second_serve_won:
            if second_serve_won >= 50:
                pts += SECOND_SERVE_WON * second_serve_won / 100
            elif second_serve_won <= 40:
                pts -= SECOND_SERVE_WON * second_serve_won / 100
            else:
                pass
        
        titles = stats.get('Titles')
        if titles:
            pts += titles * TITLES

        goat = stats.get('GOAT Rank')
        if goat:
            pts += 1 / goat * GOAT

        if odds:
            pts += ODDS * odds

        points[player] = pts
    
    p1, p2 = players

    if h2h:
        h2h_won_1 = h2h.get(p1)
        h2h_won_2 = h2h.get(p2)

        if h2h_won_1 > h2h_won_2:
            points[p1] += points[p2] / 2
        elif h2h_won_2 > h2h_won_1:
            points[p2] += points[p1] / 2
        else:
            pass

    outcome = f'{p1} got {points[p1]} and {p2} got {points[p2]}'

    return outcome, points


if __name__ == '__main__':
    pass
