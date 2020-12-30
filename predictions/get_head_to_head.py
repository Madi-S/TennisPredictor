import asyncio
import re

from time import sleep
from bs4 import BeautifulSoup

from webdriver import Webdriver


HTH = 'https://www.tennisexplorer.com/'
OUTCOME = 'https://www.tennisprediction.com/'

# Selectors:
MATCHES_SELECTOR = '.inner.noPgA'
NAV_SELECTOR = '#navlist li'



class TennisComparsion(Webdriver):

    async def get_head_to_head(self, player: str):
        await self._page._goto_retry(HTH, MATCHES_SELECTOR)
        sleep(4)
        await self._page.waitForNavigation()

        html = await self._page.content()


    async def get_outcome(self, players: list):
        await self._page._goto_retry(OUTCOME, NAV_SELECTOR)
        sleep(4)
        await self._page.waitForNavigation()

        await 
