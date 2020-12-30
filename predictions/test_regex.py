import re
from bs4 import BeautifulSoup

text = '''Name: Kaichi Uchida
Country: Japan
Birthdate: 23.08.94, 26 years ATP ranking: 329
TOP ranking's position: 237 (01.07.19, 195 points)
Points: 133
Prize money: 189.025 $
Matches total: 537
Win: 277
%: 51.58 %'''


# print(name, rank)


html = open('test.html')
soup = BeautifulSoup(html, 'html.parser')

stats = soup.find(class_='player_stats')
name = stats.find(text=re.compile(r'name', flags=re.I)).next_sibling.text
rank = stats.find(text=re.compile(r'\d+'))
rank_peak = stats.find(text=re.compile(r'TOP')).next_sibling.text

print(name, rank,rank_peak)


