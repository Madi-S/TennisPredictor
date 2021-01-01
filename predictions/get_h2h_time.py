import requests
import re

from datetime import datetime
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

URL = 'https://www.tennisexplorer.com/matches/?type=all&year={}&month={}&day={}'
UA = UserAgent()


def get_h2h_time(players: list):
    today = datetime.today()
    r = requests.get(URL.format(today.year, today.month, today.day), headers={
                     'user-agent': UA.random, 'accept-language': 'en-gb'})

    soup = BeautifulSoup(r.text, 'html.parser')
    h2h = {}
    time = None

    for player in players:
        try:
            match = soup.find(text=re.compile(
                fr'{player}')).parent.parent.parent
        except AttributeError:
            print(soup.find(text=re.compile(fr'{player}')))
            continue

        if not time:
            try:
                time = match.parent.select_one('.first.time').text.strip()
            except Exception as e:
                print(e)

        try:
            result = int(match.find(class_='h2hnbg').text.strip())

        except AttributeError:
            print(match.find(class_='h2h').text.strip())
            result = int(match.find(class_='h2h').text.strip())

        except ValueError:
            print('val')
            result = 0

        h2h[player] = result

    if time:
        return h2h, time

    return None, None


if __name__ == '__main__':
    players = players = ['Pric', 'Ganz']
    print(get_h2h_time(players))
