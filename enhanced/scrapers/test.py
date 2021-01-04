from bs4 import BeautifulSoup
import re

html = open('hau.html').read()

order = ['Ace %', 'Double Fault %', '1st Serve %','1st Serve Won %', '2nd Serve Won %', 'Break Points Saved %', 'Service Points Won %','Points Dominance', 'Games Dominance', 'Return Points Won %']


soup = BeautifulSoup(html, 'lxml')
stats = soup.select('.tab-content')[1]

for i in range(2):
	base = lambda o: stats.find(text=re.compile(fr'{o}'), class_='text-center').parent
	if i == 0:
		find = lambda o: base(o).find(class_='text-right')
	else:
		find = lambda o: base(o).find(class_='text-left')

	for o in order:
		info = find(o).text.strip()
		print(f'{o}: {info}')