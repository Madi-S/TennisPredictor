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

    return points



def get_conclusion(player1_data: dict, player2_data: dict):
    conclusion = None
    return conclusion


if __name__ == '__main__':
    data = [{1: 432}, {2134: 234}]
    print(get_conclusion(*data))
