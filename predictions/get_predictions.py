import requests

from bs4 import BeautifulSoup
from translator import translate, format_


def get_predictions(html):
    '''
    Extracts experts' predictions and useful statistics from given betting tips HTML page

    :return: a `dict` containing players, bets tendency, players' past results, detailed experts' predictions 
    '''

    def get_past_results(index):
        table = soup.find_all(class_='nohover')[index]
        imgs = table.find_all('img', attrs={'style': 'padding:2px'})[:6]

        results = list(
            map(lambda tag: '+' if 'analytics_wincell' in str(tag) else '-', imgs))
        return results

    soup = BeautifulSoup(html, 'html.parser')

    preds = soup.find_all(class_='news')

    players = [translate(tag.text.strip().replace('.', '')) for tag in soup.find_all(class_='event__info_player__name')]

    bets_tendency = [rect.get('height') for rect in soup.find(class_='highcharts-tracker').find_all('rect')][:5]
    w1, _, w2, to, tu = bets_tendency

    try:
        w1_odds, w2_odds = soup.select_one('.modeltable.top-forecast__table.top-forecast__table_border.top-forecast__table_top tbody tr').text.strip().split('\n\n\n'), 100
    except:
        try:
            odds = soup.select('.top-forecast__model tbody tr td a')[:2]
            w1_odds, w2_odds = odds[0]['title'], odds[1]['title']
        except:
            w1_odds, w2_odds = 0, 0


    predictions = {
        'Players': players,
        'Odds': {players[0]: float(w1_odds), players[1]: float(w2_odds)},
        'BetsTendency': {players[0]: float(w1), players[1]: float(w2), 'TotalOver': float(to), 'TotalUnder': float(tu)},
        'PastResults': {},
        'Predictions': []
    }

    for i, player in enumerate(players):
        predictions['PastResults'][player] = get_past_results(i)

    for pred in preds:
        try:
            info = pred.find_all(class_='info_match')[:2]

            # if 'П1' in info or 'П2' in info or 'Точный' in info[0].text:
            outcome = translate(format_(info[0].text.strip()))
            odds = float(info[1].text.strip())
            explanation = translate(pred.find_all(class_='clr')[-2].text.strip())
            expert_stats = pred.find(class_='stats').text.strip()

            predictions['Predictions'].append({'Outcome': outcome, 'Odds': odds, 'Explanation': explanation, 'ExpertStats': expert_stats})
        except Exception as e:
            print(f'Got invalid prediction {e}\n')

    with open('data.txt','w', encoding='utf-8') as f:
        f.write(str(predictions))
    return predictions


async def main():
    from get_matches import VprognozeHTML

    v = VprognozeHTML(limit=1)
    await v.init_browser()
    htmls = await v.get_matches()
    await v.shut_browser()

    predictions = []
    for html in htmls:
        predictions.append(get_predictions(html))


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
