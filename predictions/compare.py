import random
import math



def compare_players(p1: str, p2: str, p1_stats: dict, p2_stats: dict, other_stats: dict):
    calculated_probability = None # match winner pts/overall stats

    pts_1 = 0
    pts_2 = 0

    odds_1 = other_stats['Odds'][p1]
    odds_2 = other_stats['Odds'][p2]

    stats = 0

    s1 = other_stats['BetsTendency'][p1]
    s2 = other_stats['BetsTendency'][p2]
    if s1 and s2:
        if s1 > s2:
            pts_1 += 1
        elif s1 < s2:
            pts_2 += 1
        else:
            stats -= 1
        stats += 1

    s1 = other_stats['PastResults'][p1]
    s2 = other_stats['PastResults'][p2]
    if s1 and s2:
        wins_1 = [res for res in s1 if res == '+']
        wins_2 = [res for res in s2 if res == '+']

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
        if s1 >= 33:
            pts_1 -= 1
        elif s1 <= 19:
            pts_1 -= 1

        if s2 >= 33:
            pts_2 -= 1
        elif s2 <= 19:
            pts_2 -= 1

    s1 = p1_stats.get('Ranking')
    s2 = p2_stats.get('Ranking')
    if s1 and s2:
        if s1 > s2:
            pts_1 += 1
        else:
            pts_2 += 1
        stats += 1

    
    s1 = p1_stats.get('RankingPeak')
    s2 = p2_stats.get('RnakingPeak')
    if s1 and s2:
        if s1 > s2:
            pts_1 += 1
        else:
            pts_2 += 1 
        stats += 1

    # Nonsential to compare points because it is directly depends on rank

    s1 = p1_stats.get('PrizeMoney')
    s2 = p2_stats.get('PrizeMoney')
    if s1 and s2:
        # If prize money are give or take the same (do not consider this factor):
        if s1 - s2 <= 1000 and s1 - s2 >= -1000:
            stats -= 1
        elif s1 > s2:
            pts_1 += 1
        else: 
            pts_2 += 1  
        stats += 1

    s1 = p1_stats.get('TotalMatches')
    s2 = p2_stats.get('TotalMatches')
    if s1 and s2:
        # If both players have approximately the same matches amount:
        if s1 - s2 <= 10 and s1 - s2 >= -10:
            stats -= 1
        elif s1 > s2:
            pts_1 += 1
        else:
            pts_2 += 1
        stats += 1

    s1 = p1_stats.get('Winrate')
    s2 = p2_stats.get('Winrate')
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
    calculated_probability = winner / stats


    return calculated_probability