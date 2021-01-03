import requests
import re

from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver


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

def parse_html(html, players, surface):
    soup = BeautifulSoup(html, 'lxml')
    table = soup.select_one('.table.table-condensed.text-nowrap')

    data = {}
    order = [
        'H2H','Adjusted H2H', 'Age', 'Country', 'Seasons', 'Prize Money'
        'Titles', 'Current Rank', 'Best Rank', 'GOAT Rank', 'Best Season',
        'Last Appearance'
    ]
    if surface:
        order.append(surface)

    for i in range(2):
        p = players[i]
        data[p] = {}
        if i == 1:
            base = lambda o: table.find(text=re.compile(fr'{o}')).parent
            find_h2h = lambda o : base(o).next_sibling.next_sibling.a
            find_surface = lambda o: table.find(text=re.compile(fr'{o}'), class_='text-center').next_sibling.next_sibling
            find_some = lambda o : base(o).parent.next_sibling.next_sibling
            find_any = lambda o: base(o).next_sibling.next_sibling
        else:
            base = lambda o: table.find(text=re.compile(fr'{o}')).parent
            find_h2h = lambda o : base(o).previous_sibling.previous_sibling.a
            find_surface = lambda o: table.find(text=re.compile(fr'{o}'), class_='text-center').previous_sibling.previous_sibling
            find_some = lambda o : base(o).parent.previous_sibling.previous_sibling
            find_any = lambda o: base(o).previous_sibling.previous_sibling
            
        for o in order:
            print(o)
            try:
                if 'H2H' in o:
                    info = find_h2h(o) 
                elif o == 'Best Season' or o == 'Overall':
                    info = find_some(o)
                elif o in ['Hard','Grass','Clay']:
                    info = find_surface(o)
                else:
                    info = find_any(o)
                data[p][o] = info.text.strip()
            except:
                data[p][o] = None

    order = ['Ace %', 'Double Fault %', '1st Serve %','1st Serve Won %', '2nd Serve Won %', 
    'Break Points Saved %', 'Service Points Won %',
    'Points Dominance', 'Games Dominance', 'Return Points Won %']

    for i in range(0, 2):
        base = lambda d: soup.find(text=re.compile(fr'{d}'), class_='text-center')
        if i == 1:
            print('Player 2:')
            find = lambda d: base(d).parent.select_one('.text-left')
        else:
            print('Player 1:')
            find = lambda d: base(d).parent.select_one('.text-right')
        for d in data:
            data[p][o] = find(d).text.strip()

    return data


    
def compare_players(p1, p2, tournament=None, surface=None):
    id1 = get_player_id(p1)
    id2 = get_player_id(p2)

    if not (id1 and id2):
        return None

    url = 'https://www.ultimatetennisstatistics.com/headToHead?playerId1={}&playerId2={}'
    driver = webdriver.Firefox()

    with open('hau.html','w') as f:
        f.write(driver.page_source)
        print('written')
    

    if not r.ok:
        raise AttributeError(f'Bad response from UltimateTennis: {r}. Fix the issue')

    profiles = parse_html(r.text, [p1, p2], surface)
    with open('profiles.txt','w') as f:
        f.write(str(profiles))
    # stats[p1]['past_matches'] = get_past_matches(id1) 
    # stats[p2]['past_matches'] = get_past_matches(id2) 


def get_past_matches(id_):
    return 1


'''
Request URL: https://www.ultimatetennisstatistics.com/matchesTable?playerId=5324&current=1&rowCount=15&sort%5Bdate%5D=desc&searchPhrase=&season=&fromDate=&toDate=&level=&bestOf=&surface=&indoor=&speed=&round=&result=&opponent=&tournamentId=&tournamentEventId=&outcome=&score=&countryId=&bigWin=false&_=1609678509654
Request Method: GET
Status Code: 200 
Remote Address: 46.101.166.59:443
Referrer Policy: strict-origin-when-cross-origin
Cache-Control: private
Connection: keep-alive
Content-Encoding: gzip
Content-Type: application/json
Date: Sun, 03 Jan 2021 12:55:14 GMT
Expires: Thu, 01 Jan 1970 00:00:00 GMT
Keep-Alive: timeout=60
Transfer-Encoding: chunked
vary: accept-encoding
Accept: */*
Accept-Encoding: gzip, deflate, br
Accept-Language: ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7
Connection: keep-alive
Cookie: _ga=GA1.2.659216525.1609145839; _gid=GA1.2.1340506244.1609145839; __gads=ID=a110e92986bf849e-225e69d973b9003b:T=1609145842:RT=1609145842:S=ALNI_Ma4Yl3UW1qQ2GVAeX1FXzaLBttlhg; _gat=1
Host: www.ultimatetennisstatistics.com
Referer: https://www.ultimatetennisstatistics.com/playerProfile?playerId=5324
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36
X-Requested-With: XMLHttpRequest
playerId: 5324
current: 1
rowCount: 15
sort[date]: desc
searchPhrase: 
season: 
fromDate: 
toDate: 
level: 
bestOf: 
surface: 
indoor: 
speed: 
round: 
result: 
opponent: 
tournamentId: 
tournamentEventId: 
outcome: 
score: 
countryId: 
bigWin: false
_: 1609678509654
'''

'''
Response:
[{"id":"4742","value":"Rafael Nadal","label":"Rafael Nadal (ESP)"},{"id":"3970","value":"David Ferrer","label":"David Ferrer (ESP)"},{"id":"3786","value":"Nikolay Davydenko","label":"Nikolay Davydenko (RUS)"},{"id":"3900","value":"David Nalbandian","label":"David Nalbandian (ARG)"},{"id":"1434","value":"Petr Korda","label":"Petr Korda (CZE)"},{"id":"6407","value":"Daniil Medvedev","label":"Daniil Medvedev (RUS)"},{"id":"55","value":"Cliff Drysdale","label":"Cliff Drysdale (RSA)"},{"id":"5663","value":"David Goffin","label":"David Goffin (BEL)"},{"id":"4269","value":"Fernando Verdasco","label":"Fernando Verdasco (ESP)"},{"id":"1649","value":"Guillermo Perez Roldan","label":"Guillermo Perez Roldan (ARG)"},{"id":"4570","value":"Marcos Baghdatis","label":"Marcos Baghdatis (CYP)"},{"id":"1609","value":"David Wheaton","label":"David Wheaton (USA)"},{"id":"855","value":"Scott Davis","label":"Scott Davis (USA)"},{"id":"946","value":"Slobodan Zivojinovic","label":"Slobodan Zivojinovic (SRB)"},{"id":"2539","value":"Bohdan Ulihrach","label":"Bohdan Ulihrach (CZE)"},{"id":"1190","value":"Darren Cahill","label":"Darren Cahill (AUS)"},{"id":"815","value":"David Pate","label":"David Pate (USA)"},{"id":"967","value":"Dan Goldie","label":"Dan Goldie (USA)"},{"id":"1686","value":"Franco Davin","label":"Franco Davin (ARG)"},{"id":"2106","value":"Davide Sanguinetti","label":"Davide Sanguinetti (ITA)"}]
'''

if __name__ == '__main__':
    compare_players('Paire','Goffin',surface='Grass')
