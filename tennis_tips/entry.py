# Collect all matches' HTMLs and matches themselves                                 !!! DONE
# Collect all expert's predictions for collected matches from vrpognoze for today   !!! DONE
# Collect all stats from ultimate_stats and tennislive_stats                        !!! DONE
# Produce outcome and points                                                        !!! DONE
# Export everything to .docx                                                        !!! DONE

import os
import argparse
import asyncio

from get_conclusion import get_outcome
from get_predictions import get_predictions
from get_h2h_time import get_h2h_time
from logger_config import get_logger
from tennis_parser import Parser
from docx_writer import DOCXWriter


logger = get_logger()

args_parser = argparse.ArgumentParser(prog='Tennis Predictor by Madi S',
                                     usage='Specify the `limit` value for maximum amount of tennis predictions for today (5 by default).Specify the `filename` for the .docx file with predictions (TennisPredictions.docx by default)',
                                     description='Tennis Predictor based on tennis players\'s stats and form. Produces a .docx file with detailed and formatted predictions')

args_parser.add_argument('-l','--limit', choices=[i for i in range(1, 11)], help='Maximum number of tennis predictions to produce, choose between [1; 10]', default=10)
args_parser.add_argument('-f','--filename', type=str, help='Filename for the .docx file with predictions (specify without file format)', default='TennisPredictions')

args = args_parser.parse_args()



async def main():
    logger.debug('Got args: %s', args)

    writer = DOCXWriter(args.filename)

    p = Parser(limit=args.limit)
    await p.init_browser(hidden=False)

    matches_html = await p.get_matches()
    matches = []

    for i in range(len(matches_html)):
        html = matches_html.pop(0)
        matches.append(get_predictions(html))
        logger.debug('Parsing HTML #%s ', i + 1)

    for match_info in matches:
        writable = True

        logger.debug(match_info['Odds'], match_info['BetsTendency'])
        
        stats = {}
        to_write_stats = {}
        to_write_data = {}

        players = match_info['Players']

        full_names = await p.get_full_names(players)    # Dictionary

        if full_names:
            logger.debug('Full names are: %s', full_names)

            h2h, time = get_h2h_time(players,  [name.split(' ')[-1] for name in full_names.values()])
            to_write_data['H2H'] = h2h
            to_write_data['Time'] = time

            logger.debug('Head-to-head matches: %s', h2h)
            logger.debug('Match will start at %s', time)

            for player in players:
                full_name = full_names[player]
                stats[player] = {}

                data = await p.get_stats(full_name)
                if data:
                    logger.debug('Data %s updated for %s',data, player)
                    stats[player].update(data)
                    to_write_stats[player] = data
                else:
                    writable = False

                data = await p.get_detailed_stats(full_name)
                if data:
                    logger.debug('Data %s updated for %s', data, player)
                    stats[player].update(data)

            if writable:
                outcome, points = get_outcome(players, stats, match_info, h2h)
                to_write_data['Points'] = points
                to_write_data['Conclusion'] = outcome

                logger.debug('Outcome:%s\nPoints:%s', outcome, points)           

                writer.write(match_info, to_write_stats, to_write_data)
            else:
                logger.debug('Info for %s is not writable', full_names)
        else:
            logger.debug('No stats and full names found for %s. Hence, ignoring this match', players)

    await p.shut_browser()

if __name__ == '__main__':
    asyncio.run(main())
