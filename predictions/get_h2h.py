import re
import requests
from bs4 import BeautifulSoup

URL = 'https://www.tennisexplorer.com'


def get_h2h(players: list):
    r = requests.get(URL)

    soup = BeautifulSoup(r.text, 'html.parser')

    for player in players:
        match = soup.find(text=re.compile(fr'{player}'))

        if match:
            link = URL + match.parent['href']

            r = requests.get(link)

            soup = BeautifulSoup(r.text, 'html.parser')

            tag = soup.find('h2', class_='bg').text

            if ':' in tag:
                h2h = [int(res) for res in tag.split(':')[1].replace(' ', '').split('-')]
                print(h2h)

            else:
                print(tag)

