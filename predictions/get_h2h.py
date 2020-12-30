import re
import requests
from datetime import datetime
from bs4 import BeautifulSoup

URL = 'https://www.tennisexplorer.com'
ALL = '/matches/?type=all&year={}&month={}&day={}'


def get_h2h(players: list):
    '''
    Function to get head-to-head matches between given players

    param players: a `list` of players to search h2h between
    return: returns a `list` of h2h results and home player `str` or `None` if not matches or h2h were found 
    '''
    today = datetime.today()
    r = requests.get(URL + ALL.format(today.year, today.month, today.day))

    soup = BeautifulSoup(r.text, 'html.parser')

    for player in players:
        match = soup.find(text=re.compile(fr'{player}'))

        if match:
            link = URL + match.parent.parent.parent.find_all('td')[-1].find('a')['href']
            
            print(link)
            
            r = requests.get(link)

            soup = BeautifulSoup(r.text, 'html.parser')

            tag = soup.find('h2', class_='bg').text

            home = soup.find(class_='t-name').text

            if home in players[0]:
                home_player = players[0]
            else:
                home_player = players[1]

            if ':' in tag:
                h2h = [int(res) for res in tag.split(':')[
                    1].replace(' ', '').split('-')]
                return h2h, home_player

    return None


if __name__ == '__main__':
    print(get_h2h(['Yashina E', 'Oliynykova O']))
