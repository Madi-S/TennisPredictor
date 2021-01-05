import requests
import re

from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep

URL = 'https://www.ultimatetennisstatistics.com'
MATCHES = 'https://www.ultimatetennisstatistics.com/matchesTable?playerId={}&current=1&rowCount=15&sort%5Bdate%5D=desc&searchPhrase=&season=&fromDate=&toDate=&level=&bestOf=&surface=&indoor=&speed=&round=&result=&opponent=&tournamentId=&tournamentEventId=&outcome=&score=&countryId=&bigWin=false&_=1609742224223'
headers = {'Accept-Language': 'en-US', 'Referer': 'https://www.ultimatetennisstatistics.com/playerProfile?playerId=5663',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}



def get_player_id(name):
    url = 'https://www.ultimatetennisstatistics.com/autocompletePlayer?term={}'
    r = requests.get(url.format(name.replace(' ', '+')), headers=headers)

    if not r.ok:
        raise AttributeError(f'Bad response from UltimateTennis: {r}. Fix the issue')

    found = r.json()

    if not found:
        print(f'No player found for {name}')
        return 

    return found[0]['id']



def parse_html(html, players, surface):
    soup = BeautifulSoup(html, 'lxml')
    data = {}

    stats = soup.select_one('.table.table-condensed.text-nowrap')
    order = [
        'H2H','Adjusted H2H', 'Age', 'Country', 'Seasons', 'Prize Money',
        'Titles', 'Current Rank', 'Best Rank', 'GOAT Rank', 'Best Season',
        'Last Appearance', 'Overall'
    ]
    winrates = ['Overall','grass','clay','hard']
    if surface:
        order.append(surface)

    base = lambda o: stats.find(text=re.compile(fr'{o}'), class_='text-center').parent
    wr = lambda o: stats.find(text=re.compile(fr'{o}', flags=re.I), class_='text-center')
    for i in range(2):
        p = players[i]
        data[p] = {}

        if i == 0:
            locate = lambda o: base(o).find(class_='text-right')
            winrate = lambda o: wr(o).previous_sibling.previous_sibling
        else:
            locate = lambda o: base(o).find(class_='text-left')
            winrate = lambda o: wr(o).next_sibling.next_sibling

        for o in order:
            if o in winrates:
                data[p][o] = winrate(o).text.strip()
            else:
                data[p][o] = locate(o).text.strip().replace('\n',' ')

    stats = soup.select('.tab-content')[1]
    order = ['Ace %', 'Double Fault %', '1st Serve %','1st Serve Won %', '2nd Serve Won %', 
    'Break Points Saved %', 'Service Points Won %',
    'Points Dominance', 'Games Dominance', 'Return Points Won %']

    for i in range(0, 2):
        p = players[i]

        if i == 0:
            find = lambda o: base(o).find(class_='text-right')
        else:
            find = lambda o: base(o).find(class_='text-left')
        
        for o in order:
            data[p][o] = find(o).text.strip()

    return data


    
def get_players_data(p1, p2, surface=None):
    id1 = get_player_id(p1)
    id2 = get_player_id(p2)

    if not (id1 and id2):
        print(f'No IDs found for {p1} and {p2}')
        return None

    url = 'https://www.ultimatetennisstatistics.com/headToHead?playerId1={}&playerId2={}'

    driver = webdriver.Firefox(service_log_path='NUL')
    driver.get(url.format(id1, id2))
    sleep(4)

    # click on statistics
    stats_b = driver.find_elements_by_class_name('dropdown-toggle')[-1]
    stats_b.click()

    show_b = driver.find_element_by_id('statisticsPill')
    show_b.click() 

    sleep(4)
    html = driver.page_source

    driver.close()
    driver.quit()

    stats = parse_html(html, [p1, p2], surface)
    stats[p1]['past_matches'] = get_past_matches(id1, p1) 
    stats[p2]['past_matches'] = get_past_matches(id2, p2) 

    return stats



def get_past_matches(id_, player):
    r = requests.get(MATCHES.format(id_))

    if not r.ok:
        raise AttributeError(f'Bad response from UltimateTennis: {r}. Fix the issue') 

    return [{'won': player in res['winner']['name'], 'score': res['score'], 'winner': res['winner']['name'], 'loser': res['loser']['name']} for res in r.json()['rows'][:10]]

if __name__ == '__main__':
    data = get_players_data('Paire', 'Goffin', surface='grass')
    with open('players_data.txt','w') as f:
        f.write(str(data))