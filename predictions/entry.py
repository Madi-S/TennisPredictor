# Collect all matches' HTMLs and matches themselves                                 !!! DONE
# Collect all expert's predictions for collected matches from vrpognoze for today   !!! DONE
# Collect all stats from ultimate_stats and tennislive_stats
# Format all given text
# Export everything to .docx

import os
import asyncio

from get_conclusion import get_conclusion, get_points
from get_predictions import get_predictions
from get_h2h import get_h2h
from logger_config import get_logger
from tennis_parser import Parser
# from docx_writer.writer import Writer


async def main():
    p = Parser()
    await p.init_browser()

    # Extract HTMLs of present for today tennis matches
    htmls = await p.get_matches()

    # For each match get predictions from vprognoze
    predictions = []
    for html in htmls:
        predictions.append(get_predictions(html))

    # Loop through each prediction -> player -> get stats for him/her
    for prediction in predictions:
        players_data = []

        # Get full names to correctly get tennis stats
        players = prediction['Players']
        full_names = p.get_full_names(players)

        # Get head-to-head matches
        h2h = get_h2h(player)

        # Overall expert's picks
        total_over = prediction['BetsTendency']['TotalOver']
        total_under = prediction['BetsTendency']['TotalUnder']
        overall_picks = prediction['BetsTendency'][players[0]
                                                   ] + prediction['BetsTendency'][players[1]]
        experts_preds = prediction['Predictions']

        points

        # Collect tennis stats for each player and count his/her overall points based on extracted stats
        for i, player in enumerate(players):
            # os.mkdir(player)
            winner_odds = prediction['Odds'][player]
            past_results = prediction['PastResults'][player]
            winner_picks = prediction['BetsTendency'][player]
            winner_pick_ratio = winner_picks[i] / overall_picks

            full_name = full_names[i]

            player_stats = p.get_stats(full_name)
            detailed_stats = p.get_detailed_stats(full_name)

            points[player] = get_points(past_results, winner_odds, winner_pick_ratio, **player_stats)

        # counted_prediction = p.get_counted_outcome(full_names)
        conclusion = get_conclusion(points, total_over, total_under, h2h, experts_preds)

    await p.shut_browser()

if __name__ == '__main__':
    asyncio.run(main())
