from bs4 import BeautifulSoup
import re

html = open('test.html').read()


soup = BeautifulSoup(html, 'lxml')

#order = [
#        'H2H','Adjusted H2H', 'Age', 'Country', 'Seasons', 'Prize Money',
#        'Titles', 'Current Rank', 'Best Rank', 'GOAT Rank', 'Best Season',
#        'Last Appearance', 'Overall', 'Grass', 'Hard','Clay'
#    ]
#table = soup.select_one('.table.table-condensed.text-nowrap')
#for o in order:
#	print(f'{o}:', end='')
#	if 'H2H' in o:
#		info = table.find(text=re.compile(fr'{o}')).parent.next_sibling.next_sibling.a.text.strip()
#	elif o == 'Best Season' or o == 'Overall':
#		info = table.find(text=re.compile(fr'{o}')).parent.parent.next_sibling.next_sibling.text.strip()
#	elif o in ['Hard','Grass','Indoor','Clay']:
#		info = table.find(text=re.compile(fr'{o}'), class_='text-center').next_sibling.next_sibling.text.strip()
#	else:
#		info = table.find(text=re.compile(fr'{o}')).parent.next_sibling.next_sibling.text.strip()
#
#	print(info)

data = ['Ace %', 'Double Fault %', '1st Serve %',
 '1st Serve Won %', '2nd Serve Won %', 'Break Points Saved %', 'Service Points Won %',
'Points Dominance', 'Games Dominance', 'Return Points Won %']

for i in range(0, 2):
	base = lambda d: soup.find(text=re.compile(fr'{d}'), class_='text-center')
	if i == 1:
		print('Player 2:')
		find = lambda d: base(d).parent.select_one('.text-left').text
	else:
		print('Player 1:')
		find = lambda d: base(d).parent.select_one('.text-right').text
	for d in data:
		info = find(d)
		print(d,info)
