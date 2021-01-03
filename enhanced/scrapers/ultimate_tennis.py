import requests

from time import sleep
from datetime import datetime
from random import shuffle
from bs4 import BeautifulSoup


URL = 'https://www.ultimatetennisstatistics.com'

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


def get_stats(id_):
    url = 'https://www.ultimatetennisstatistics.com/playerProfile?playerId={}'
    r = requests.get(url.format(id_), headers=headers)

    if not r.ok:
        raise AttributeError(f'Bad response from UltimateTennis: {r}. Fix the issue')



'''
Request headers:
Accept: application/json, text/javascript, */*; q=0.01
Accept-Encoding: gzip, deflate, br
Accept-Language: ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7
Connection: keep-alive
Cookie: _ga=GA1.2.659216525.1609145839; _gid=GA1.2.1340506244.1609145839; __gads=ID=a110e92986bf849e-225e69d973b9003b:T=1609145842:RT=1609145842:S=ALNI_Ma4Yl3UW1qQ2GVAeX1FXzaLBttlhg
Host: www.ultimatetennisstatistics.com
Referer: https://www.ultimatetennisstatistics.com/playerProfile?playerId=5663
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36
X-Requested-With: XMLHttpRequest
term: Da
'''

'''
Response:
[{"id":"4742","value":"Rafael Nadal","label":"Rafael Nadal (ESP)"},{"id":"3970","value":"David Ferrer","label":"David Ferrer (ESP)"},{"id":"3786","value":"Nikolay Davydenko","label":"Nikolay Davydenko (RUS)"},{"id":"3900","value":"David Nalbandian","label":"David Nalbandian (ARG)"},{"id":"1434","value":"Petr Korda","label":"Petr Korda (CZE)"},{"id":"6407","value":"Daniil Medvedev","label":"Daniil Medvedev (RUS)"},{"id":"55","value":"Cliff Drysdale","label":"Cliff Drysdale (RSA)"},{"id":"5663","value":"David Goffin","label":"David Goffin (BEL)"},{"id":"4269","value":"Fernando Verdasco","label":"Fernando Verdasco (ESP)"},{"id":"1649","value":"Guillermo Perez Roldan","label":"Guillermo Perez Roldan (ARG)"},{"id":"4570","value":"Marcos Baghdatis","label":"Marcos Baghdatis (CYP)"},{"id":"1609","value":"David Wheaton","label":"David Wheaton (USA)"},{"id":"855","value":"Scott Davis","label":"Scott Davis (USA)"},{"id":"946","value":"Slobodan Zivojinovic","label":"Slobodan Zivojinovic (SRB)"},{"id":"2539","value":"Bohdan Ulihrach","label":"Bohdan Ulihrach (CZE)"},{"id":"1190","value":"Darren Cahill","label":"Darren Cahill (AUS)"},{"id":"815","value":"David Pate","label":"David Pate (USA)"},{"id":"967","value":"Dan Goldie","label":"Dan Goldie (USA)"},{"id":"1686","value":"Franco Davin","label":"Franco Davin (ARG)"},{"id":"2106","value":"Davide Sanguinetti","label":"Davide Sanguinetti (ITA)"}]
'''

if __name__ == '__main__':
    print(find_player('David G'))
