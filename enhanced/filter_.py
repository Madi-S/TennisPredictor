


def filter_matches(matches):
    '''
    Not doubles
    Not WTA
    Has tournament
    Has detailed stats
    ''' 
    filtered = []
    secondary = []
    for match in matches:
        if match['p1'] and match['p2']:
            # There is `/` in doubles:
            if not ('/' in match['p1'] or '/' in match['p2']):
                if match['time_gmt']:
                    if match['p1_odds'] and match['p2_odds']:
                        if match['tournament_info']:
                            if match['tournament_info']['male']:
                                prize = match['tournament_info']['prize_pool']
                                if prize:
                                    if prize > 100000:
                                        print(f'!!!Decent match found {match["p1"]} vs {match["p2"]}')
                                        filtered.append(match)  
                                    else:
                                        secondary.append(match)
                                        print(f'Little prize pool {prize} for {match["p1"]} vs {match["p2"]}')
                                else:
                                    print(f'No prize pool for {match["p1"]} vs {match["p2"]}')
                            else:
                                print(f'Not male match: {match["p1"]} vs {match["p2"]}')
                        else:
                            print(f'No tournament info {match["p1"]} vs {match["p2"]}')
                    else:
                        print(f'No odds for {match["p1"]} vs {match["p2"]}')
                else:
                    print(f'No time specified for {match["p1"]} vs {match["p2"]}')
            else:
                print(f'Doubles found {match["p1"]} vs {match["p2"]}')
        else:
            print('No players\' names')
    if len(filtered) < 6:
        while len(filtered) < 6 and secondary:
            filtered.append(secondary.pop()) 
    return filtered


