import asyncio
import pyppeteer


from screeninfo import get_monitors
from pyppeteer import launch
from random import uniform
from time import sleep


class Webdriver:
    _monitor = get_monitors()[0]
    _viewport = {'width': _monitor.width, 'height': _monitor.height, }

    async def init_browser(self, hidden: bool = False):
        '''
        Initializing browser by opening pages, setting headers and parameters before starting lead generaiton

        :param hidden: Run Webdriver in headless mode
        :return: returns nothing
        '''
        self.browser = await launch(
            {'dumpio': True,'ignoreHTTPSErrors': True, 'headless': hidden, 'args': ['--start-maximized']},
        )
        self._page = (await self.browser.pages())[0]

        await self._page.setViewport(self._viewport)
        await self._page.reload()

    async def shut_browser(self):
        '''
        Gracefully shut down pyppeteer webdriver in 10 seconds

        :return: returns nothing
        '''
        sleep(10)
        await self._page.close()
        await self.browser.close()

    async def _do_retry(self, operation, xpath: str, dest=None, retries=0):
        '''
        Keep doing `operation` until `xpath` can be located

        :param operation: Function that must be executed until `xpath` can be located
        :param xpath: Xpath that should be found after `operation` has been executed
        :param dest=None: Destination for `opration`, e.g., `operation` = click and `dest` = yellow_button. Hence, yellow_button will be clicked 
        :param retries=0: No need to specify, unless number of retries must be decreased
        :return: returns nothing
        '''
        if retries >= 10:
            raise SystemError(
                'Max 10 retries exceeded when clicking the place')
        try:
            if dest:
                await operation(dest)
            else:
                await operation()
            sleep(uniform(1, 1.5))
            await self._page.waitForXPath(xpath, {'visible': True})
        except pyppeteer.errors.TimeoutError:
            await self._do_retry(operation, xpath, dest, retries + 1)
        except:
            pass

    async def _goto_retry(self, url: str, selector: str = None, xpath: str = None, retries: int = 0):
        '''
        Keep going to `url` until `selector` can be located

        :param url: URL to request for
        :param selector: CSS Selector that should be found after `operation` has been executed, if not specified -> waitForNavigation()
        :param xpath: XPATH that should be found after `operation` has been executed. Do not specify `xpath` with `selector` and vice versa
        :param retries=0: No need to specify, unless number of retries must be decreased
        :return: `True` for successfull request and Raises `SystemError` for exceeding retries amount
        '''
        while retries <= 10:
            try:
                await self._page.goto(url)
                if xpath:
                    await self._page.waitForXPath(xpath)
                elif selector:
                    await self._page.waitForSelector(selector)
                else:
                    await self._page.waitForNavigation()
                print('Breaked from while loop -> positive response\n')
                return True
            except:
                retries += 1
        raise SystemError('Max 10 retries exceeded when clicking the place')
