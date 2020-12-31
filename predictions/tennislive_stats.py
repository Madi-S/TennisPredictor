import asyncio
import re
import os

from fake_useragent import UserAgent
from screeninfo import get_monitors
from pyppeteer import launch
from bs4 import BeautifulSoup
from random import uniform
from time import sleep

from webdriver import Webdriver


URL = 'https://www.tennislive.net/atp/ranking/'
SPACE = '            '

# Locators:
SEARCH_XPATH = '//*[@alt="search"]'
TYPE_XPATH = '//*[@class="f_text"]'
STATS_XPATH = '//*[@class="player_stats"]'
PLAYER_SELECTOR = '#show_players a'
TABLE_XPATH = '//*[@class="player_matches"]'
STATS_CLS = 'player_stats'


class TennisLiveStats(Webdriver):

    async def get_stats(self, player_name: str):
        '''
        Scrape tennislive.net for given `player_name` stats

        :param player_name: Player name -`str` to search for
        :return: returns `dict` with stats and `player_name` stats or `None` if no stats for `player_name` were found
        '''

        def _get_json(html):
            soup = BeautifulSoup(html, 'html.parser')
            stats = soup.find(class_=STATS_CLS).text.strip()

            stats = soup.find(class_='player_stats')
            
            name = stats.find(text=re.compile(r'name', flags=re.I)).next_sibling.text.strip()

            try:
                age = int(stats.find(text=re.compile(r'Birthdate')).next_sibling.text.split(',')[-1].replace(' ','').replace('years',''))
            except:
                age = None

            try:
                rank = int(stats.find(text=re.compile(r'ATP')).next_element.next_element.text.strip())
            except:
                rank = None

            try:
                rank_peak = int(stats.find(text=re.compile(r'TOP')).next_sibling.text.strip())
            except:
                rank_peak = None

            try:
                points = int(stats.find(text=re.compile(r'Points')).next_sibling.text.strip())
            except:
                points = None

            try:
                prize_money = int(stats.find(text=re.compile(r'Prize')).next_sibling.text.replace(' ','').replace('$','').replace('.',''))
            except:
                prize_money = None  

            try:
                matches = int(stats.find(text=re.compile(r'Matches total')).next_sibling.text.replace(' ',''))
            except:
                matches = None

            try:
                winrate = float(stats.find(text=re.compile(r'%')).next_sibling.text.replace(' ','').replace('%',''))
            except:
                winrate = None

            return {
                'Name': name,
                'Age': age,
                'Ranking': rank,
                'RankingPeak': rank_peak,
                'Points': points,
                'PrizeMoney': prize_money,
                'TotalMatches': matches,
                'Winrate%': winrate,
            }

        print(f'Gathering stats for {player_name}\n')
        try:
            await self._page.goto(URL)
        except:
            await self._page.goto(URL)
        sleep(4)
        await self._page.waitForXPath(SEARCH_XPATH)

        await (await self._page.xpath(SEARCH_XPATH))[0].click()
        sleep(0.5)

        await (await self._page.xpath(TYPE_XPATH))[0].click()
        sleep(0.5)

        for letter in player_name:
            await self._page.keyboard.type(letter)
            sleep(0.11)

        sleep(2.5)

        try:
            player = await self._page.querySelector(PLAYER_SELECTOR)
            await self._do_retry(player.click, STATS_XPATH)
        except:
            print(f'No info for player {player_name}\n')
            return None

        sleep(4)

        html = await self._page.content()
        data = _get_json(html)
        print(data)
        return data

        # os.chdir(player_name)
        # table = await self._page.xpath(TABLE_XPATH)
        # await table[1].screenshot({'path': f'{player_name}_tennislive_stats.png'})
        # print('Screenshot created\n')



async def main():
    players = ['Uchida K', 'Mansuri S', 'Echargui M', 'Djokovic N',
               'Raonic M', 'Rafel N', 'Medvedev D', 'Rublev A']

    t = TennisLiveStats()
    await t.init_browser()
    for plr in players:
        await t.get_stats(plr)
    await t.shut_browser()

if __name__ == '__main__':
    asyncio.run(main())
