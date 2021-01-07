import argparse

from tennis_explorer import get_matches_info
from ultimate_tennis import get_players_data
from compare import compare_players
from filter_ import filter_matches


# parser = argparse.ArgumentParser()
LIMIT = 7

def main():
    raw_matches = get_matches_info()
    matches = filter_matches(raw_matches)
    print(f'Total matches: {len(matches)}, filtered: {len(raw_matches)}')
    for match in matches:
        p1, p2 = match['p1'], match['p2']
        odds1, odds2 = match['p1_odds'], match['p2_odds']

        print(f'{p1} ({odds1}) vs {p2} ({odds2})')

        surface = match['tournament_info']['surface']

        stats = get_players_data(p1, p2, surface)
        with open('data.txt','w', encoding='utf-8') as f:
            f.write(f'{p1} ({odds1}) vs {p2} ({odds2})' + str(stats) + '\n\n')

        if stats:
            winner, prob = compare_players(match, stats)
            print(winner, prob)




if __name__ == "__main__":
    main()