import asyncio

from time import sleep
from bs4 import BeautifulSoup

from webdriver import Webdriver


URL = 'https://vprognoze.ru/topforecast/?utm_referrer='
TENNIS_VALUE = '2'


class VprognozeHTML(Webdriver):

    def __init__(self, limit: int = 5):
        '''

        :param limit=5: Get at maximum 5 HTML of matches' pages
        :return: returns nothing
        '''
        if not (limit > 0 and limit < 11 and isinstance(limit, int)):
            raise TypeError(
                '`Limit` value must be an integer between 1 and 10')
        self._limit = limit

    async def get_matches(self):
        '''
        Collects HTMLs of all betting tips for tennis (if present) pages from vprognoze

        :return: returns a `list` of HTMLs, which does not exceed specified limit, if no matches are present for today returns `False`
        '''
        if not '_page' in self.__dict__:
            raise ValueError(
                'Initialize the browser before searching by `await .init_broswser()`')

        await self._goto_retry(URL, selector='.button_default')
        # await self._page.goto(URL)
        # sleep(4)
        # await self._page.waitForSelector('.button_default')

        try:
            await asyncio.gather(
                self._page.waitForNavigation(),
                self._page.click('.button_default'),
            )
        except:
            self.get_matches()

        await self._page.select('#sport', TENNIS_VALUE)

        await asyncio.gather(
            self._page.waitForNavigation(),
            self._page.click('.button_default'),
        )
        print('Final button clicked\n')

        return await self._get_htmls()

    async def _get_htmls(self):
        html = await self._page.content()
        soup = BeautifulSoup(html, 'lxml')

        matches = soup.find_all(class_='top-forecast__match-name')[:self._limit]
        urls = [match.find('a').get('href') for match in matches]

        print(f'{len(urls)} Extracted URLs: {urls}\n')
        htmls = []

        for url in urls:
            await self._goto_retry(url, selector='.event__info_player__name')
            sleep(3)

            htmls.append(await self._page.content())
            print(f'HTML was appended: {url}\n')

        return htmls


async def main():
    e = VprognozeHTML()
    await e.init_browser()
    await e.get_matches()
    await e.shut_browser()

if __name__ == '__main__':
    asyncio.run(main())
