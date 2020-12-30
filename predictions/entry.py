# Collect all matches' HTMLs and matches themselves                                 !!! DONE
# Collect all expert's predictions for collected matches from vrpognoze for today   !!! DONE
# Collect all stats from ultimate_stats and tennislive_stats
# Create folders for each player to save imgs, stats there
# Colect last tweets and IG posts of players
# Format all given text
# Export everything to .docx

import os
import asyncio

from get_predictions import get_predictions
from get_conclusion import get_conclusion
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
        real_names = []

        players = prediction['Players']

        to = prediction['BetsTendency']['TotalOver']
        tu = prediction['BetsTendency']['TotalUnder']
        preds = prediction['Predictions'] 
        # odds = [pred['Odds'] for pred in prediction['Predictions']]
        # outcomes = [pred['Outcome'] for pred in prediction['Predictions']]

        for i , player in enumerate(players):  
            os.mkdir(player)
            past_results = prediction['PastResults'][player]
            winner_picks = prediction['BetsTendency'][player]

            player_stats = p.get_stats(player)
            real_names.append(player_stats['Name'])

            detailed_stats = p.get_detailed_stats(player)


            data = None
            players_data.append(data)
        
        counted_prediction = p.get_counted_outcome(real_names)

        conclusion = get_conclusion(*players_data)





    await p.shut_browser()

if __name__ == '__main__':
    asyncio.run(main())
