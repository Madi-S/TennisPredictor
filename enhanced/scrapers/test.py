from bs4 import BeautifulSoup

html = open('test.html', encoding='utf-8').read()
soup = BeautifulSoup(html, 'lxml')

table = soup.find(class_='result')
players = table.find_all(attrs={'onmouseover': 'md_over(this);'})
print(len(players))
t = players[-10].find_previous_sibling(class_='flags').find('a').get('href')
print(t)
