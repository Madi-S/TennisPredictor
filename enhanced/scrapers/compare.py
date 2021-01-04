import random
import math


def compare_players(match_data: dict, players_data: dict):
    calculated_probability = None  # match winner pts/overall stats

    p1 = match_data.get('p1')
    p2 = match_data.get('p2')
    
    p1_stats = players_data.get(p1)
    p2_stats = players_data.get(p2)

    odds1 = int(match_data.get('p1_odds'))
    odds2 = int(match_data.get('p2_odds'))

    tournament = match_data.get('tournament_info')
    if tournament:
        surface = tournament.get('surface')
        location = tournament.get('location')

    pts_1 = 0
    pts_2 = 0
    stats = 0

    s1 = p1_stats.get('past_matches')
    s2 = p2_stats.get('past_matches')
    if s1 and s2:
        wins_1 = 0
        for i, res in enumerate(s1):
            if res.get('won'):
                wins_1 += 1 / (i + 1)
            else:
                wins_1 -= 1 / (i + 1)

        wins_2 = 0
        for i, res in enumerate(s2):
            if res.get('won'):
                wins_2 += 1 / (i + 1)
            else:
                wins_2 -= 1 / (i + 1)

        if wins_1 > wins_2:
            pts_1 += 1
        elif wins_1 < wins_2:
            pts_2 += 1
        else:
            stats -= 1
        stats += 1

    s1 = p1_stats.get('Age')
    s2 = p2_stats.get('Age')
    if s1 and s2:
        s1 = int(s1)
        s2 = int(s2)

        if s1 >= 33:
            pts_1 -= 1
        elif s1 <= 19:
            pts_1 -= 1

        if s2 >= 33:
            pts_2 -= 1
        elif s2 <= 19:
            pts_2 -= 1

    s1 = p1_stats.get('Current Rank')
    s2 = p2_stats.get('Current Rank')
    if s1 and s2:
        s1 = int(s1.split('(')[0].replace(' ',''))
        s2 = int(s2.split('(')[0].replace(' ',''))

        if s1 > s2:
            pts_1 += 1
        else:
            pts_2 += 1
        stats += 1

    s1 = p1_stats.get('RankingPeak')
    s2 = p2_stats.get('RnakingPeak')
    if s1 and s2:
        s1 = int(s1.split('(')[0].replace(' ','')) 
        s2 = int(s2.split('(')[0].replace(' ','')) 

        if s1 > s2:
            pts_1 += 1
        else:
            pts_2 += 1
        stats += 1

    # Nonsential to compare points because it is directly depends on rank

    s1 = p1_stats.get('Prize Money')
    s2 = p2_stats.get('Prize Money')
    if s1 and s2:
        s1 = int(s1.split('$')[-1].replace(',',''))
        s2 = int(s2.split('$')[-1].replace(',',''))

        # If prize money are give or take the same (do not consider this factor):
        if s1 - s2 <= 5000 and s1 - s2 >= -5000:
            stats -= 1
        elif s1 > s2:
            pts_1 += 1
        else:
            pts_2 += 1
        stats += 1

    # s1 = p1_stats.get('TotalMatches')
    # s2 = p2_stats.get('TotalMatches')
    # if s1 and s2:
    #     # If both players have approximately the same matches amount:
    #     if s1 - s2 <= 10 and s1 - s2 >= -10:
    #         stats -= 1
    #     elif s1 > s2:
    #         pts_1 += 1
    #     else:
    #         pts_2 += 1
    #     stats += 1

    s1 = p1_stats.get('Overall')
    s2 = p2_stats.get('Overall')
    if s1 and s2:
        # If winrate is approximately the same:
        if s1 - s2 <= 1.5 and s1 - s2 >= -1.5:
            stats -= 1
        elif s1 > s2:
            pts_1 += 1
        else:
            pts_2 += 1
        stats += 1

    s1 = p1_stats.get('Ace %')
    s2 = p2_stats.get('Ace %')
    if s1 and s2:
        # If Ace % is give or take the same:
        if s1 - s2 <= 0.5 and s1 - s2 >= -0.5:
            stats -= 1
        elif s1 > s2:
            pts_1 += 1
        else:
            pts_2 += 1
        stats += 1

    s1 = p1_stats.get('Fault %')
    s2 = p2_stats.get('Fault %')
    if s1 and s2:
        # Lesser the double fault %, the better for the player:
        # If both players approximately concede the same number of double faults:
        if s1 - s2 <= 0.5 and s1 - s2 >= -0.5:
            stats -= 1
        elif s1 < s2:
            p1_stats += 1
        else:
            p2_stats += 1
        stats += 1

    s1 = p1_stats.get('1st Serve %')
    s2 = p2_stats.get('1st Serve %')
    if s1 and s2:
        # If 1st serve ration is the same:
        if s1 - s2 <= 2.5 and s2 - s1 >= -2.5:
            stats -= 1
        elif s1 > s2:
            pts_1 += 1
        else:
            pts_2 += 1
        stats += 1

    s1 = p1_stats.get('1st Serve Won %')
    s2 = p2_stats.get('2nd Serve Won %')
    if s1 and s2:
        # If both players have the same 1st win %:
        if s1 - s2 <= 2.5 and s1 - s2 >= -2.5:
            stats -= 1
        elif s1 > s2:
            pts_1 += 1
        else:
            pts_2 += 1
        stats += 1

    s1 = p1_stats.get('2nd Serve Won %')
    s2 = p2_stats.get('2nd Serve Won %')
    if s1 and s2:
        # If both players have the same 2nd serve win %:
        if s1 - s2 <= 2.5 and s1 - s2 >= -2.5:
            stats -= 1
        elif s1 > s2:
            pts_1 += 1
        else:
            pts_2 += 1
        stats += 1

    s1 = p1_stats.get('Titles')
    s2 = p2_stats.get('Titles')
    if s1 and s2:
        if s1 == s2:
            stats -= 1
        elif s1 > s2:
            pts_1 += 1
        else:
            pts_2 += 1
        stats += 1

    s1 = p1_stats.get('GOAT Rank')
    s2 = p2_stats.get('GOAT Rank')
    if s1 and s2:
        # If both players are close in GOAT ranking
        if s1 - s2 <= 5 and s2 - s1 >= -5:
            stats -= 1
        elif s1 > s2:
            pts_1 += 1
        else:
            pts_2 += 1
        stats += 1

    winner = max([pts_1, pts_2])

    if winner == pts_1:
        odds = odds.get(p1)
    else:
        odds = odds.get(p2)

    calculated_probability = winner / stats * 100

    return winner, calculated_probability
