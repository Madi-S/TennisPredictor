import asyncio

from time import sleep
from bs4 import BeautifulSoup

from webdriver import Webdriver


URL = 'https://vprognoze.ru/topforecast/?utm_referrer='
TENNIS_VALUE = '2'


class VprognozeHTML(Webdriver):

    def __init__(self, limit: int):
        '''

        :param limit: Get at maximum given `int` number of HTML of matches' pages from vprognoze/topforecasts
        :return: returns nothing
        '''
        self._limit = limit

    async def get_matches(self, date=None):
        '''
        Collects HTMLs of all betting tips for tennis (if present) pages from vprognoze

        :return: returns a `list` of HTMLs, which does not exceed specified limit, if no matches are present for today returns `False`
        '''
        if not '_page' in self.__dict__:
            raise ValueError('Initialize the browser before searching by `await .init_broswser()`')

        await self._goto_retry(URL, selector='.button_default')
        # await self._page.goto(URL)
        # sleep(4)
        # await self._page.waitForSelector('.button_default')

        sleep(5)
        await self._page.waitForSelector('.button_default')
        await self._page.click('.button_default')
        sleep(5)
        await self._page.waitForSelector('.button_default')
        await self._page.select('#sport', TENNIS_VALUE)
        print('selected')
        sleep(2)

        if date:
            await self._page.click('#int_time', options={'clickCount':3})
            sleep(1.5)
            await self._page.keyboard.type(date)
            sleep(1.5)

        try:
            await self._page.click('.button_default')
            await self._page.waitForNavigation()
        except:
            await self._page.click('.button_default')
            sleep(5)           

        return await self._get_htmls()

    async def _get_htmls(self):
        print('Get_htmls was called\n')
        html = await self._page.content()
        soup = BeautifulSoup(html, 'lxml')

        matches = soup.find_all(class_='top-forecast__match-name')
        urls = [match.find('a').get('href') for match in matches]

        print(f'{len(urls)} Extracted URLs: {urls}\n')
        htmls = []

        for url in urls:
            await self._goto_retry(url, selector='.event__info_player__name')
            sleep(3)
            soup = BeautifulSoup(await self._page.content(), 'lxml')
            header = soup.find('h1')
            if not 'WTA' in header.text:
                htmls.append(await self._page.content())
                print(f'HTML was appended: {url}\n')
            else:
                print(f'WTA Match found -> ignoring: {url}\n')

        print(f'Returning {len(htmls)}\n')
        return htmls[:self._limit]


async def main():
    e = VprognozeHTML(limit=5)
    await e.init_browser()
    await e.get_matches()
    await e.shut_browser()

if __name__ == '__main__':
    asyncio.run(main())
