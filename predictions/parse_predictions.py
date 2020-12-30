



def parse_predictions(players: list, preds: list):
    points = {players[0]: int(), players[1]: int()}
    for pred in preds:
        points += pred

    return points



    