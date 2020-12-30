import re
from bs4 import BeautifulSoup

with open('web.html', 'r') as f:
	html = f.read()

soup = BeautifulSoup(html, 'lxml')
stats = soup.find(class_='tab-content')
ingame_stats = ['Ace %','Double Fault %','1st Serve %','1st Serve Won %', '2nd Serve Won %']

data = {}

data['GOATRank'] = int(stats.find(text=re.compile(r'GOAT Rank')).next_element.next_sibling.text.split(' ')[0])



for stat in ingame_stats:
	try:
		data[stat] = int(stats.find(text=re.compile(r'Ace %')).next_sibling.text.replace('%',''))
	except:
		data[stat] = None # or 0

print(ace_percent)

