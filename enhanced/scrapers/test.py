from bs4 import BeautifulSoup
import re
html = open('stats.html').read()
soup = BeautifulSoup(html, 'lxml')

stats = soup.select_one('.table.table-condensed.text-nowrap')
a =  stats.find(text=re.compile(fr'Overall'), class_='text-center').next_sibling.next_sibling.text
print(a)

