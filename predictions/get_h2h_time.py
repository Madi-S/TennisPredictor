import requests
import re

from datetime import datetime
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

URL = 'https://www.tennisexplorer.com/matches/?type=all&year={}&month={}&day={}'
UA = UserAgent()


def get_h2h_time(players: list):
    # today = datetime.today()
    # r = requests.get(URL.format(today.year, today.month, today.day), headers={
    #                  'user-agent': UA.random, 'accept-language': 'en-gb'})
    # with open('test.html', 'w', encoding='utf-8') as f:
    #     f.write(r.text)
    with open('test.html', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')
    h2h = {}
    time = None

    for player in players:

        try:
            match = soup.find(string=re.compile(
                fr'{player}')).parent.parent.parent
            h2h[player] = int(match.find(class_='h2h').text)
            time = match.select_one('.first.time').text.strip()
        except AttributeError:
            pass

    if time:
        return h2h, time
        
    return None, None


print(get_h2h_time(['Pichleer', 'Kotzen']))
