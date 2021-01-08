import requests
import re

from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from datetime import datetime


MATCHES = 'https://www.tennisexplorer.com/matches/?type={}&year={}&month={}&day={}'

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
        info = soup.select_one('#center .box.boxBasic.lGray').text.strip()
        if '$' in info:
            info = info.split('$')
        elif '€':
            info = info.split('€')
    except:
        info = None
    try:
        male = not 'women' in ''.join(info).lower()
    except:
        male = None
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
    try:
        title = soup.find('h1').text.strip()
    except:
        title = None

    if surface == 'indoor':
        print('Indoor transformed to Hard')
        surface = 'hard'

    return {'title': title, 'prize_pool': prize, 'male': male, 'surface': surface, 'location': location, 'link': link}


def get_player_name(url):
    r = requests.get('https://www.tennisexplorer.com' + url)
    soup = BeautifulSoup(r.text, 'lxml')
    name = soup.find('h3').text.strip()
    return name


def parse_html(html, limit):
    soup = BeautifulSoup(html, 'lxml')

    table = soup.find(class_='tab-menu')

    matches_data = []
    players = table.find_all(attrs={'onmouseover': 'md_over(this);'})
    for i, player in enumerate(players):
        if i % 2 == 0:
            data = {}

            try:
                player.find(class_='result').text
                print('Match ended')
                data['p1'] = None
                data['p2'] = None
                continue
            except:
                pass

            try:
                link = player.find_previous_sibling(
                    class_='flags').find('a')['href']
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
                player_url = player.find(class_='t-name').find('a').get('href')
                data['p1'] = get_player_name(player_url)
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
                player_url = player.find(class_='t-name').find('a').get('href')
                data['p2'] = get_player_name(player_url)
            except:
                data['p2'] = None
            try:
                data['p2_h2h'] = int(player.find(
                    class_=re.compile(r'h2h')).text.strip())
            except:
                data['p2_h2h'] = None
            print(i, data['p1'], data['p2'])
            matches_data.append(data)


    return matches_data[:limit]


