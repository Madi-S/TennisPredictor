import asyncio
import re

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
        Scrape tennislive.net for given `player_name` statistics

        :param player_name: Player name
        :return: returns screenshot with stats and `player_name` statistics ot `False` if no statistics for `player_name` were found
        '''

        def _get_json_data(html):
            soup = BeautifulSoup(html, 'html.parser')
            stats = soup.find(class_=STATS_CLS).text.strip()

            name = stats.find('a').text.strip()


            #return {
            #    'Name': name,
            #    'Age': age,
            #    'Ranking': rank,
            #    'RankingPeak': rank_peak,
            #    'Points': points,
            #    'PrizeMoney': prize_money,
            #    'TotalMatches': matches,
            #    'Wins': wins,
            #    'Winrate%': winrate,
            #}

        print(f'Gathering stats for {player_name}\n')
        try:
            await self._page.goto(URL)
        except:
            await self._page.goto(URL)
        sleep(4)
        await self._page.waitForXPath(SEARCH_XPATH)
        print('On the main page\n')

        await (await self._page.xpath(SEARCH_XPATH))[0].click()
        sleep(0.5)
        print('Clicked on search button\n')

        await (await self._page.xpath(TYPE_XPATH))[0].click()
        sleep(0.5)
        print('Clicked on search bar\n')

        for letter in player_name:
            await self._page.keyboard.type(letter)
            sleep(0.11)

        sleep(2.5)
        print('Entered player\'s name\n')

        try:
            player = await self._page.querySelector(PLAYER_SELECTOR)
            await self._do_retry(player.click, STATS_XPATH)
            print('Clicked on first match\n')
        except:
            print(f'No info for player {player_name}\n')
            return False

        sleep(4)
        print('Done with waiting\n')

        html = await self._page.content()
        self._parse(html)

        table = await self._page.xpath(TABLE_XPATH)
        await table[1].screenshot({'path': f'{player_name}_tennislive_stats.png'})
        print('Screenshot created\n')

    def _parse(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        stats = soup.find(class_=STATS_CLS).text.strip().replace(SPACE, '\n')
        with open('stats.txt','w') as f:
            f.write(stats)
        print('\n', stats, '\n')


async def main():
    players = ['Uchida K', 'Mansuri S', 'Echargui M', 'Novak Djokovic',
               'Raonic Mil', 'Rafel N', 'Medvedev D', 'Rublev A']

    t = TennisLiveStats()
    await t.init_browser()
    for plr in players:
        await t.get_stats(plr)
    await t.shut_browser()

if __name__ == '__main__':
    asyncio.run(main())
