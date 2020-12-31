import asyncio

from time import sleep
from bs4 import BeautifulSoup

from webdriver import Webdriver


URL = 'https://www.ultimatetennisstatistics.com/'

STATS = ['profile', 'season', 'events', 'matches', 'timeline',
         'rivalries', 'ranking', 'tournaments', 'goatPoints', 'records']




class UltimateStats(Webdriver):
    def __init__(self):
        pass

    async def _search_name(self, player_name: str):
        await self._page.click('#player')
        print('Cliked on search bar\n')

        for letter in player_name:
            await self._page.keyboard.type(letter)
            sleep(0.11)
        print('Done typing\n')
        sleep(3)

        await asyncio.gather(
            self._page.waitForNavigation(),
            self._page.click('.ui-menu-item'),
        )
        # await self._page.click('.ui-menu-item')
        print('Clicked on first match\n')
        sleep(2.5)


    async def get_full_names(self, names: list):
        '''
        Extract full names from tennislive for given `list` of partial names

        :param names: `list` of partial names, where each name's type is `str`
        :return: returns a `dict` of full names and partial names as key-value pairs or `None` if nothing found 
        '''
        if not '_page' in self.__dict__:
            raise ValueError('Initialize the browser before searching by `await .init_broswser()`')

        print(f'Gathering full names for: {" ".join(names)}\n')

        try:
            await self._page.goto(URL)
        except:
            await self._page.goto(URL)

        sleep(2.5)
        print('Successful navigation\n')

        full_names = {}
        for name in names:
            await self._search_name(name)
            html = await self._page.content()
            soup = BeautifulSoup(html, 'html.parser')
            full_name = soup.find('h3').text.strip() 
            full_names[name] = full_name

        return full_names


    async def get_detailed_stats(self, player_name: str):
        '''
        Scrape ultimatetennisstatistics.com for given `player_name` statistics

        :param player_name: Player name
        :return: returns path to PDF document with stats and `player_name` statistics ot `False` if no statistics for `player_name` were found
        '''
        if not '_page' in self.__dict__:
            raise ValueError('Initialize the browser before searching by `await .init_broswser()`')

        print(f'Gathering stats for {player_name}\n')

        try:
            await self._page.goto(URL)
        except:
            await self._page.goto(URL)

        sleep(2.5)
        print('Successful navigation\n')

        await self._search_name(player_name)

        profile = await self._page.querySelector('.tab-content')
        await profile.screenshot({'path': f'{player_name}_ultimatetennis_profile.png'})

        # for stat in STATS:
        #     await self._page.click(f'#{stat}Pill')
        #     sleep(2.5)
        #     stats = await self._page.querySelector('.tab-content')
        #     await stats.screenshot({'path': f'{player_name}_ultimatetennis_{stat}.png'})
        #     print(f'Screenshot for {stat} created\n')





async def main():
    players = ['Uchida K', 'Mansuri S', 'Echargui M', 'Novak Djokovic',
           'Raonic Mil', 'Rafel N', 'Medvedev D', 'Rublev A']

    # t = UltimateStats()
    # await t.init_browser()
    # for plr in players:
    #     await t.get_detailed_stats(plr)
    # await t.shut_browser()

    t = UltimateStats()
    await t.init_browser()
    full_names = await t.get_full_names(players)
    print(full_names)
    await t.shut_browser()


if __name__ == '__main__':
    asyncio.run(main())
