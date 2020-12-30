import re
import requests
from bs4 import BeautifulSoup

url = 'https://www.tennisexplorer.com'

r = requests.get(url)

soup = BeautifulSoup(r.text, 'lxml')

match = soup.find(text=re.compile(r'Husaric A'))

if match:
    link = url + match.parent['href']
    r = requests.get(link)

    soup = BeautifulSoup(r.text, 'lxml')
    tag = soup.find('h2',class_='bg').text
    if ':' in tag:
        h2h = [int(res) for res in tag.split(':')[1].replace(' ','').split('-')]
        print(h2h)

