import asyncio
import re

from time import sleep
from bs4 import BeautifulSoup

from webdriver import Webdriver


URL = 'https://www.tennisexplorer.com/'


# Selectors:
MATCHES_SELECTOR = '.inner.noPgA'



class TennisExplorer(Webdriver):

    async def get_head_to_head(self, player: str):
        await self._page._goto_retry(URL, MATCHES_SELECTOR)
        sleep(4)
        await self._page.waitForNavigation()

        html = await self._page.content()

