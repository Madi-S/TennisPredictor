# Collect all matches' HTMLs and matches themselves                                 !!! DONE
# Collect all expert's predictions for collected matches from vrpognoze for today   !!! DONE
# Collect all stats from ultimate_stats and tennislive_stats                        !!! DONE
# Format all given text
# Export everything to .docx

import os
import asyncio

from get_conclusion import get_conclusion, get_outcome
from get_predictions import get_predictions
from get_h2h_time import get_h2h_time
from logger_config import get_logger
from tennis_parser import Parser
from docx_writer import DOCXWriter


logger = get_logger()




async def test():
    writer = DOCXWriter()

    p = Parser(limit=1)
    await p.init_browser()
    
    matches_html = await p.get_matches()
    matches = []

    for html in matches_html:
        matches.append(get_predictions(html))

    logger.debug(matches)
    
    for match_info in matches:
        stats = {}

        players = match_info['Players']

        full_names = await p.get_full_names(players)    # Dictionary

        if full_names:
            logger.debug('Full names are: %s', full_names)

            h2h, time = get_h2h_time([name.split(' ')[-1] for name in full_names])
            logger.debug('Head-to-head matches: %s', h2h)
            logger.debug('Matchin will start at %s', time)

            for player in players:
                full_name = full_names[player]
                stats[player] = {}

                data = await p.get_stats(full_name)
                if data:
                    print(f'Data {data} updated for {player}')
                    stats[player].update(data)

                data = await p.get_detailed_stats(full_name) 
                if data:
                    print(f'Data {data} updated for {player}')
                    stats[player].update(data)

            with open('data.txt','w') as f:
                f.write(str(players) + '\n')
                f.write(str(stats) + '\n')
                f.write(str(match_info) +'\n')
                f.write(str(h2h) + '\n')

            # outcome, points = get_outcome(players, stats, match_info, h2h)
            # logger.debug(outcome, points)
            # logger.debug('Outcome:%s\nPoints:%s', outcome, points) 
            # conclusion = get_conclusion(stat)

            # writer.write(data)


            logger.debug(stats)
        else:
            logger.debug('No stats and full names found for %s', players)


    await p.shut_browser()

if __name__ == '__main__':
    asyncio.run(test())
