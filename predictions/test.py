import re
from bs4 import BeautifulSoup

html = open('test.html',encoding='utf-8').read()
INGAME_STATS = ['Ace %', 'Double Fault %',
                '1st Serve %', '1st Serve Won %', '2nd Serve Won %']
soup = BeautifulSoup(html, 'html.parser')

for stat in INGAME_STATS:
    tag = soup.find(text=re.compile(fr'{stat}')).parent.next_sibling.next_sibling.text
    print(tag)
    break