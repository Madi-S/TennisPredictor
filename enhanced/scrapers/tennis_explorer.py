import requests
import re

from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from datetime import datetime
from random import sample, shuffle


URL = 'https://www.tennisexplorer.com/matches/'
ATP_SINGLES = 'https://www.tennisexplorer.com/matches/?type=atp-single&year={}&month={}&day={}'

ua = UserAgent()
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'cache-control': 'max-age=0',
    'accept-language': 'en-US',
}


def get_tournament_info(tournament_link):
    link = 'https://www.tennisexplorer.com' + tournament_link
    r = requests.get(link)
    soup = BeautifulSoup(r.text, 'lxml')

    try:
        info = soup.select_one(
            '#center .box.boxBasic.lGray').text.strip().split('$')
    except:
        info = None
    try:
        prize = float(info[0].replace(
            '(', '').replace(' ', '').replace(',', ''))
    except:
        prize = None
    try:
        surface = info[1].replace(' ', '').split(',')[1].lower()
    except:
        surface = None
    try:
        location = soup.select_one('#center .bg').text.strip().split(
            '(')[-1].replace(')', '')
    except:
        location = None

    if surface == 'indoor':
        print('Indoor transformed to Hard')
        surface = 'hard'

    return {'prize_pool': prize, 'surface': surface, 'location': location, 'link': link}


def parse_html(html, limit):
    soup = BeautifulSoup(html, 'lxml')

    table = soup.find(class_='result')

    matches_data = []
    players = table.find_all(attrs={'onmouseover': 'md_over(this);'})
    for i, player in enumerate(players):
        # print(i, player)
        if i % 2 == 0:
            data = {}
            try:
                link = player.find_previous_sibling(
                    class_='flags').find('a').get('href')
                data['tournament_info'] = get_tournament_info(link)
            except:
                data['tournament_info'] = None
            try:
                data['time_gmt'] = player.find(class_='time').text.strip()
            except:
                data['time_gmt'] = None
            try:
                data['match_link'] = 'https://www.tennisexplorer.com' + \
                    player.find(
                        attrs={'title': 'Click for match detail'}).get('href')
            except:
                data['match_link'] = None
            try:
                data['p1'] = player.find(
                    class_='t-name').find('a').text.strip()
            except:
                data['p1'] = None
            try:
                data['p1_h2h'] = int(player.find(
                    class_=re.compile(r'h2h')).text.strip())
            except:
                data['p1_h2h'] = None

            odds = player.find_all(class_=re.compile(r'course'))
            try:
                data['p1_odds'] = float(odds[0].text.strip())
            except:
                data['p1_odds'] = None
            try:
                data['p2_odds'] = float(odds[1].text.strip())
            except:
                data['p2_odds'] = None
        else:
            try:
                data['p2'] = player.find(
                    class_='t-name').find('a').text.strip()
            except:
                data['p2'] = None
            try:
                data['p2_h2h'] = int(player.find(
                    class_=re.compile(r'h2h')).text.strip())
            except:
                data['p2_h2h'] = None
            matches_data.append(data)

    shuffle(matches_data)
    return matches_data[:limit]


def get_matches_info(limit: int = 5):
    headers['user-agent'] = ua.random

    today = datetime.today()
    link = ATP_SINGLES.format(today.year, today.month, today.day)

    print(link)

    r = requests.get(link, headers=headers)

    if not r.ok:
        raise AttributeError(
            f'Bad response from TennisExplorer: {r}. Fix the issue')

    matches = parse_html(r.text, limit)
    return matches


if __name__ == '__main__':
    matches = get_matches_info(limit=1000)
    print(matches)
    with open('matches.txt','w') as f:
    	f.write(str(matches))
