import re
import requests
from bs4 import BeautifulSoup

url = 'https://www.tennisexplorer.com/'

r = requests.get(url)

print(r)
soup = BeautifulSoup(r.text, 'lxml')

match = soup.find(text=re.compile(r''))