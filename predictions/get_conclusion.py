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
HIGH_FIRST_SERVE = 50
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
                    pts += 1 / (i + 1) * PREVIOUS_MATCH
                else:
                    pts += 1 / (i + 1) * (-PREVIOUS_MATCH)

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
        print(h2h, p1, p2)
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
    players = ['Mansuri S', 'Takeuchi K']
    players_stats = {'Mansuri S': {'Name': 'Skander Mansouri', 'Age': 25, 'Ranking': 385, 'RankingPeak': 303, 'Points': 105, 'PrizeMoney': 79759, 'TotalMatches': 267, 'Winrate%': 61.8, 'Titles': None, 'GOAT Rank': None, 'Ace %': None, 'Double Fault %': None, '1st Serve %': None, '1st Serve Won %': None, '2nd Serve Won %': None},
                     'Takeuchi K': {'Name': 'Kento Takeuchi', 'Age': 33, 'Ranking': 711, 'RankingPeak': 378, 'Points': 29, 'PrizeMoney': 167515, 'TotalMatches': 813, 'Winrate%': 52.89, 'Titles': None, 'GOAT Rank': None, 'Ace %': 0.0, 'Double Fault %': 4.7, '1st Serve %': 41.9, '1st Serve Won %': 38.9, '2nd Serve Won %': 32.0}}
    betting_stats = {'Players': ['Mansuri S', 'Takeuchi K'], 'Odds': {'Mansuri S': 1.1, 'Takeuchi K': 6.2}, 'BetsTendency': {'Mansuri S': 72.0, 'Takeuchi K': 217.0, 'TotalOver': 0.0, 'TotalUnder': 0.0}, 'PastResults': {'Mansuri S': ['+', '+', '+', '+', '+', '+'], 'Takeuchi K': ['+', '+', '-', '-', '-', '+']}, 'Predictions': [{'Outcome': 'WINNER 2', 'Odds': 6.7, 'Explanation': "The coefficient drops, because they gave 7.5 at all, but even 6.7 is incredibly high, value a huge one.I would not give more than 2.5-3 for the Japanese here and Mansuri's victory is in principle dangerous to take in the tournament.In the first round he could fly away to young Kumar in two sets, but he did not apply for the match, gave a set and fell apart in the third.Today, the weaker Gregg drank blood.Had a set chance, but didn't finish 3-0.In general, Mansuri has noticeably played enough lately, especially", 'ExpertProfit%': 0.0}, {
        'Outcome': 'Handicap2 by sets (1.5)', 'Odds': 2.66, 'Explanation': 'One set is given a coefficient that should go for the whole match.As I said, Mansuri has played enough over the past weeks and looks weak on this Monastir.In the first round I had to fly off in two sets and today there were many problems against a far from strong opponent.The Japanese, in turn, recently started his season, but is already showing a good game.For two laps I have not experienced any problems.In general, he is a strong player, therefore', 'ExpertProfit%': 0.0}, {'Outcome': 'Handicap2 by games (7)', 'Odds': 1.71, 'Explanation': 'Well, the handicap is also incredibly wild.The level of the players at the peak is approximately equal.But the Japanese beeches are apparently underestimated due to the fact that he recently started the season.There were injuries, but I seem to have returned in good shape.Two laps confidently passed, although the rivals were not the strongest.But at the same time, Mansuri almost flew out of the similar.As for me, I recently won the futures and played enough.Here you need a desire to fight for victory against the Japanese, and even less such a head start', 'ExpertProfit%': 0.0}]}
    h2h = {'Mansuri S': 0, 'Takeuchi K': 0}
    print(get_outcome(players, players_stats, betting_stats, h2h))
