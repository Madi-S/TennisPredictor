import random
from datetime import datetime


def compare_players(match_data: dict, players_data: dict):
    calculated_probability = None  # match winner pts/number of comparisons 

    p1 = match_data.get('p1')
    p2 = match_data.get('p2')
    
    p1_stats = players_data.get(p1)
    p2_stats = players_data.get(p2)

    try:
        odds_1 = float(match_data.get('p1_odds'))
        odds_2 = float(match_data.get('p2_odds'))
    except:
        odds_1 = 1
        odds_2 = 1

    tournament = match_data.get('tournament_info')
    surface = 'foo'
    location = 'bar'
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
            print(f'{p1} won past_matches')
            pts_1 += 1
        elif wins_1 < wins_2:
            print(f'{p2} won past_matches')
            pts_2 += 1
        else:
            print('??? past_matches')
            stats -= 1
        stats += 1


    s1 = p1_stats.get('Country')
    s2 = p2_stats.get('Country')
    if s1 and s2:
        if s1.lower() == location.lower():
            print(f'{p1} won country')
            pts_1 += 1
        if s2.lower() == location.lower():
            pts_2 += 1
            print(f'{p2} won country')
        else:
            print('??? location country')


    s1 = p1_stats.get('Age')
    s2 = p2_stats.get('Age')
    if s1 and s2:
        s1 = int(s1.split(' ')[0])
        s2 = int(s2.split(' ')[0])

        if s1 >= 34:
            print(f'{p1} too old')
            pts_1 -= 1
        elif s1 <= 18:
            print(f'{p1} too young')
            pts_1 -= 1

        if s2 >= 34:
            print(f'{p2} too old')
            pts_2 -= 1
        elif s2 <= 18:
            pts_2 -= 1
            print(f'{p2} too young')

    # 'Current Rank': '28 (1738)', 'Best Rank': '18 (11-01-2016)'

    s1 = p1_stats.get('Current Rank')
    s2 = p2_stats.get('Current Rank')
    if s1 and s2:
        s1 = -int(s1.split(' ')[0])
        s2 = -int(s2.split(' ')[0])
        if s1 > s2:
            print(f'{p1} won current_rank')
            pts_1 += 1
        else:
            print(f'{p2} won current_rank')
            pts_2 += 1
        stats += 1

    s1 = p1_stats.get('RankingPeak')
    s2 = p2_stats.get('RankingPeak')
    if s1 and s2:
        s1 = -int(s1.split(' ')[0])
        s2 = -int(s2.split(' ')[0])
        print(s1, s2)
        if s1 - s2 <= 2 and s1 - s2 >= -2:
            print('??? ranking peak')
            stats -= 1
        if s1 > s2:
            print(f'{p1} won rank_peak')
            pts_1 += 1
        else:
            print(f'{p2} won rank_peak')
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
            print('??? prize money')
            stats -= 1
        elif s1 > s2:
            print(f'{p1} won prize')
            pts_1 += 1
        else:
            print(f'{p2} won prize')
            pts_2 += 1
        stats += 1



    s1 = p1_stats.get('Overall')
    s2 = p2_stats.get('Overall')
    if s1 and s2:
        
        # For winrate:
        t1, t2 = s1, s2
        s1 = float(t1.split(' ')[0].replace('%',''))
        s2 = float(t2.split(' ')[0].replace('%',''))
        # If winrate is approximately the same:
        if s1 - s2 <= 1.5 and s1 - s2 >= -1.5:
            print('??? overall winrate')
            stats -= 1
        elif s1 > s2:
            print(f'{p1} won winrate')
            pts_1 += 1
        else:
            print(f'{p2} won winrate')
            pts_2 += 1
        stats += 1
        # For total matches:
        s1 = int(t1.split(' ')[1].split('-')[0].replace('(',''))
        s2 = int(t2.split(' ')[1].split('-')[0].replace('(',''))
        # If both players have approximately the same number of wins:
        if s1 - s2 <= 10 and s1 - s2 >= -10:
            print('??? total wins')
            stats -= 1
        elif s1 > s2:
            print(f'{p1} won total wins')
            pts_1 += 1
        else:
            print(f'{p2} won total wins')
            pts_2 += 1
        stats += 1

    s1 = p1_stats.get('Seasons')
    s2 = p2_stats.get('Seasons')
    if s1 and s2:
        s1 = int(s1)
        s2 = int(s2)

        # If both players almost the same number of seasons:
        if s1 - s2 <= 1 and s1 - s2 >= -1:
            print('??? seasons')
            stats -= 1
        elif s1 > s2:
            print(f'{p1} won seasons')
            pts_1 += 1
        else:
            print(f'{p2} won seasons')
            pts_2 += 1
        stats += 1

    s1 = p1_stats.get('Titles')
    s2 = p2_stats.get('Titles')
    if s1 and s2:
        if s1 == s2:
            print('??? titles')
            stats -= 1
        elif s1 > s2:
            print(f'{p1} won titles')
            pts_1 += 1
        else:
            print(f'{p2} won titles')
            pts_2 += 1
        stats += 1

    s1 = p1_stats.get('H2H')
    s2 = p2_stats.get('H2H')
    if s1 and s2:
        s1 = float(s1.split('(')[-1].replace('%)',''))
        s2 = float(s2.split('(')[-1].replace('%)',''))

        if s1 == s2:
            print('??? h2h')
            stats -= 1
        elif s1 > s2:
            print(f'{p1} won h2h')
            pts_1 += 1
        else:
            print(f'{p2} won h2h')
            pts_2 += 1
        stats += 1

    s1 = p1_stats.get('Adjusted H2H')
    s2 = p2_stats.get('Adjusted H2H')
    if s1 and s2:
        s1 = float(s1.split(' ')[0])
        s2 = float(s2.split(' ')[0])

        if s1 == s2:
            print('??? adjusted h2h')
            stats -= 2
        elif s1 > s2:
            print(f'{p1} won adj h2h')
            pts_1 += 2
        else:
            print(f'{p2} won adj h2h')
            pts_2 += 2
        stats += 2
         

    s1 = p1_stats.get('Best Season')
    s2 = p2_stats.get('Best Season')
    if s1 and s2:
        year = datetime.today().year
        s1 = year - int(s1)
        s2 = year - int(s2)

        if s1 == s2:
            print('??? best season')
            stats -= 1
        elif s1 < s2:
            print(f'{p1} won best season')
            pts_1 += 1
        else:
            print(f'{p2} won best season')
            pts_2 += 1
        stats += 1 

    s1 = p1_stats.get('Last Appearance')
    s2 = p2_stats.get('Last Appearance')
    if s1 and s2:
        s1 = s1.split(' ')[0].split('-')
        s2 = s2.split(' ')[0].split('-')
        
        s1 = datetime(int(s1[2]), int(s1[1]), int(s1[0]), 0, 0, 0).timestamp()
        s2 = datetime(int(s2[2]), int(s2[1]), int(s2[0]), 0, 0, 0).timestamp()

        # If both players played relatively equal time ago
        if s1 - s2 <= 87000 and s1 - s2 >= -87000:
            stats -= 1
        elif s1 > s2:
            pts_1 += 1
        else:
            pts_2 += 1
        stats += 1


    s1 = p1_stats.get(surface)
    s2 = p2_stats.get(surface)
    if s1 and s2:
        s1 = float(s1.split('%')[0])
        s2 = float(s2.split('%')[0])

        # If winrate on given surface is approximately the same:
        if s1 - s2 <= 1.5 and s1 - s2 >= -1.5:
            print(f'??? surface winrate {surface}')
            stats -= 1
        elif s1 > s2:
            print(f'{p1} won surface winrate')
            pts_1 += 1
        else:
            print(f'{p2} won surface winrate')
            pts_2 += 1
        stats += 1

    s1 = p1_stats.get('GOAT Rank')
    s2 = p2_stats.get('GOAT Rank')
    if s1 and s2:
        s1 = -int(s1.split(' ')[0])
        s2 = -int(s2.split(' ')[0])
        print(s1, s2, s1 - s2)

        # If both players are close in GOAT ranking
        if s1 - s2 <= 5 and s1 - s2 >= -5:
            print('??? goat rank')
            stats -= 1
        elif s1 > s2:
            print(f'{p1} won GOAT Rank')
            pts_1 += 1
        else:
            print(f'{p2} won GOAT Rank')
            pts_2 += 1
        stats += 1

    s1 = p1_stats.get('Ace %')
    s2 = p2_stats.get('Ace %')
    if s1 and s2:
        s1 = float(s1.replace('%',''))
        s2 = float(s2.replace('%',''))

        if s1 - s2 <= 0.4 and s1 - s2 >= -0.4:
            print('??? ace %')
            stats -= 1
        elif s1 > s2:
            print(f'{p1} won Ace %')
            pts_1 += 1
        else:
            print(f'{p2} won Ace %')
            pts_2 += 1
        stats += 1


    s1 = p1_stats.get('Double Fault %')
    s2 = p2_stats.get('Double Fault %')
    if s1 and s2:
        s1 = float(s1.replace('%',''))
        s2 = float(s2.replace('%',''))

        # Lesser the double fault %, the better for the player:
        # If both players approximately concede the same number of double faults:
        if s1 - s2 <= 0.4 and s1 - s2 >= -0.4:
            print('??? double fault %')
            stats -= 1
        elif s1 < s2:
            print(f'{p1} won Double Fault')
            pts_1 += 1
        else:
            print(f'{p2} won Double Fault')
            pts_2 += 1
        stats += 1

    s1 = p1_stats.get('1st Serve %')
    s2 = p2_stats.get('1st Serve %')
    if s1 and s2:
        s1 = float(s1.replace('%',''))
        s2 = float(s2.replace('%',''))

        # If 1st serve ration is the same:
        if s1 - s2 <= 1.5 and s1 - s2 >= -1.5:
            print('??? 1st serve %')
            stats -= 1
        elif s1 > s2:
            print(f'{p1} won 1st serve %')
            pts_1 += 1
        else:
            print(f'{p2} won 1st serve %')
            pts_2 += 1
        stats += 1

    s1 = p1_stats.get('1st Serve Won %')
    s2 = p2_stats.get('1nd Serve Won %')
    print(f'1st serve won %: {p1_stats["1st Serve Won %"]} and {p2_stats["1st Serve Won %"]}')
    if s1 and s2:
        s1 = float(s1.replace('%',''))
        s2 = float(s2.replace('%',''))

        # If both players have the same 1st win %:
        if s1 - s2 <= 1.5 and s1 - s2 >= -1.5:
            print('??? 1st serve won')
            stats -= 1
        elif s1 > s2:
            print(f'{p1} won 1st serve won %')
            pts_1 += 1
        else:
            print(f'{p2} won 1st serve won %')
            pts_2 += 1
        stats += 1

    s1 = p1_stats.get('2nd Serve Won %')
    s2 = p2_stats.get('2nd Serve Won %')
    if s1 and s2:
        s1 = float(s1.replace('%',''))
        s2 = float(s2.replace('%',''))

        # If both players have the same 2nd serve win %:
        if s1 - s2 <= 2 and s1 - s2 >= -2:
            print('??? 2nd serve won %')
            stats -= 1
        elif s1 > s2:
            print(f'{p1} won 2st serve won %')
            pts_1 += 1
        else:
            print(f'{p2} won 2st serve won %')
            pts_2 += 1
        stats += 1


    s1 = p1_stats.get('Break Points Saved %')
    s2 = p2_stats.get('Break Points Saved %')
    if s1 and s2:
        s1 = float(s1.replace('%',''))
        s2 = float(s2.replace('%',''))

        # If both players have the same bp saved %:
        if s1 - s2 <= 1.5 and s1 - s2 >= -1.5:
            print('??? bp saved %')
            stats -= 1
        elif s1 > s2:
            print(f'{p1} won bp saved %')
            pts_1 += 1
        else:
            print(f'{p2} won bp saved %')
            pts_2 += 1
        stats += 1

    s1 = p1_stats.get('Service Points Won %')
    s2 = p2_stats.get('Service Points Won %')
    if s1 and s2:
        s1 = float(s1.replace('%',''))
        s2 = float(s2.replace('%',''))

        # If both players have the same serivec points won %:
        if s1 - s2 <= 0.5 and s1 - s2 >= -0.5:
            print('??? service points won')
            stats -= 1
        elif s1 > s2:
            print(f'{p1} won service points won %')
            pts_1 += 1
        else:
            print(f'{p2} won service points won %')
            pts_2 += 1
        stats += 1

    s1 = p1_stats.get('Return Points Won %')
    s2 = p2_stats.get('Return Points Won %')
    if s1 and s2:
        s1 = float(s1.replace('%',''))
        s2 = float(s2.replace('%',''))

        # If both players have the same return points won %:
        if s1 - s2 <= 0.3 and s1 - s2 >= -0.3:
            print('??? return points won %')
            stats -= 1
        elif s1 > s2:
            print(f'{p1} won return points won %')
            pts_1 += 1
        else:
            print(f'{p2} won return points won %')
            pts_2 += 1
        stats += 1

    s1 = p1_stats.get('Points Dominance')
    s2 = p2_stats.get('Points Dominance')
    if s1 and s2:
        s1 = float(s1)
        s2 = float(s2)

        # If both players have the same points dominance %:
        if s1 - s2 <= 0.02 and s1 - s2 >= -0.02:
            print('??? points dominance')
            stats -= 1
        elif s1 > s2:
            print(f'{p1} won points dominance')
            pts_1 += 1
        else:
            print(f'{p2} won points dominance')
            pts_2 += 1
        stats += 1


    s1 = p1_stats.get('Games Dominance')
    s2 = p2_stats.get('Games Dominance')
    if s1 and s2:
        s1 = float(s1)
        s2 = float(s2)

        # If both players have the games dominance %:
        if s1 - s2 <= 0.02 and s1 - s2 >= -0.02:
            print('??? Games dominance')
            stats -= 1
        elif s1 > s2:
            print(f'{p1} won games dominance')
            pts_1 += 1
        else:
            print(f'{p2} won games dominance')
            pts_2 += 1
        stats += 1
       

    winner = max([pts_1, pts_2])
    if pts_1 > pts_2:
        winner = (p1, pts_1)
    elif pts_1 < pts_2:
        winner = (p2, pts_2)
    else:
        i = random.randint(0,1)
        winner = ([p1,p2][i], [pts_1, pts_2][i])


    calculated_probability = round(winner[1] / stats * 100, 1)
    with open('predictions.txt','a') as f:
        f.write(f'{p1} {pts_1} {odds_1} vs {p2} {pts_2} {odds_2}: Winner: {winner}, probability: {calculated_probability}\n\n')

    return winner, calculated_probability


if __name__ == '__main__':
    from ultimate_tennis import get_players_data
    
    data = get_players_data('Paire', 'Goffin', surface='hard')
    with open('data.txt','w') as f:
        f.write(str(data))
    match_data = {'p1': 'Paire', 'p2': 'Goffin', 'p1_odds': 1.98, 'p2_odds': 1.98, 'tournament_info':{'surface': 'hard','location':'Belgium'}}

    winner, prob = compare_players(match_data,data)
    print(winner, prob)