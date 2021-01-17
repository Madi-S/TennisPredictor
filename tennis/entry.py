from filter_ import filter_matches
from tennis_explorer import get_matches_info
from ultimate_tennis import get_players_data
from compare import compare_players
from writer import DOCXWriter


LIMIT = 100


def main():
    w = DOCXWriter('Tennis_Predictions')

    raw_matches = get_matches_info()
    matches = filter_matches(raw_matches)[:LIMIT]

    print(f'Total matches: {len(raw_matches)}, filtered: {len(matches)}')

    outcomes = []

    for match in matches:
        p1, p2 = match['p1'], match['p2']
        odds1, odds2 = match['p1_odds'], match['p2_odds']
        print(f'{p1} ({odds1}) vs {p2} ({odds2})')

        surface = match['tournament_info']['surface']
        stats = get_players_data(p1, p2, surface)
        if stats:
            winner, prob, pts_1, pts_2 = compare_players(match, stats)
            print(winner, prob)
            if winner:
                if pts_1 > 3 or pts_2 > 3:
                    outcomes.append((p1, p2, odds1, odds2, winner[0], prob, match['time_gmt'], match['tournament_info']['title']))
                    print(p1, p2, odds1, odds2, winner[0], prob, match['time_gmt'], match['tournament_info']['title'])

    while outcomes:
        w.write(*outcomes.pop(0))
    print('Done\nUse Tennis_Predictions.docx file to view tennis predictions for today')


if __name__ == '__main__':
    main()
