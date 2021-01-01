import requests
import re

from datetime import datetime
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

URL = 'https://www.tennisexplorer.com/matches/?type=all&year={}&month={}&day={}'
UA = UserAgent()


def get_h2h_time(players: list, surnames: list):
    today = datetime.today()
    r = requests.get(URL.format(today.year, today.month, today.day), headers={
                     'user-agent': UA.random, 'accept-language': 'en-gb'})

    soup = BeautifulSoup(r.text, 'html.parser')
    h2h = {}
    time = None

    for i in range(2):
        try:
            match = soup.find(text=re.compile(fr'{surnames[i]}')).parent.parent.parent
        except AttributeError:
            continue

        if not time:
            try:
                time = match.parent.select_one('.first.time').text.strip()
            except:
                pass

        try:
            result = int(match.find(class_='h2hnbg').text.strip())

        except AttributeError:
            result = int(match.find(class_='h2h').text.strip())

        except ValueError:
            result = 0

        h2h[players[i]] = result

    if time:
        return h2h, time

    return None, None


if __name__ == '__main__':
    players = players = ['Pric', 'Ganz']
    print(get_h2h_time(players))
