import asyncio

from time import sleep
from bs4 import BeautifulSoup

from webdriver import Webdriver


URL = 'https://www.ultimatetennisstatistics.com/'

STATS = ['profile', 'season', 'events', 'matches', 'timeline',
         'rivalries', 'ranking', 'tournaments', 'goatPoints', 'records']

# Locators:
SEARCH_SELECTOR = '#player'
STATS_SELECTOR = '.tab-content'
RESULT_SELECTOR = '.ui-menu-item'


class UltimateStats(Webdriver):
    def __init__(self):
        pass

    async def get_detailed_stats(self, player_name: str):
        '''
        Scrape ultimatetennisstatistics.com for given `player_name` statistics

        :param player_name: Player name
        :return: returns path to PDF document with stats and `player_name` statistics ot `False` if no statistics for `player_name` were found
        '''
        print(f'Gathering stats for {player_name}\n')
        try:
            await self._page.goto(URL)
        except:
            await self._page.goto(URL)
        sleep(4)
        print('Successful navigation\n')

        await self._page.click(SEARCH_SELECTOR)
        print('Cliked on search bar\n')

        for letter in player_name:
            await self._page.keyboard.type(letter)
            sleep(0.11)
        print('Done typing\n')
        sleep(5)

        await asyncio.gather(
            self._page.waitForNavigation(),
            self._page.click(RESULT_SELECTOR),
        )
        # await self._page.click(RESULT_SELECTOR)
        print('Clicked on first match\n')

        profile = await self._page.querySelector(STATS_SELECTOR)
        await profile.screenshot({'path': f'{player_name}_ultimatetennis_profile.png'})

        for stat in STATS:
            await self._page.click(f'#{stat}Pill')
            sleep(2)
            stats = await self._page.querySelector(STATS_SELECTOR)
            await stats.screenshot({'path': f'{player_name}_ultimatetennis_{stat}.png'})
            print(f'Screenshot for {stat} created\n')


players = ['Uchida K', 'Mansuri S', 'Echargui M', 'Novak Djokovic',
           'Raonic Mil', 'Rafel N', 'Medvedev D', 'Rublev A']


async def main():
    t = UltimateStats()
    await t.init_browser()
    for plr in players:
        await t.get_detailed_stats(plr)
    await t.shut_browser()


if __name__ == '__main__':
    asyncio.run(main())
