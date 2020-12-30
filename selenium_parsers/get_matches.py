from time import sleep
from datetime import datetime
from random import shuffle
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException


class Webdriver:
    def __init__(self):
        self._driver = webdriver.Firefox(service_log_path='NUL')
        self._driver.maximize_window()

    def kill(self):
        sleep(5)
        self._driver.close()
        self._driver.quit()

    def get_htmls(self, limit=5):
        self._driver.get('https://vprognoze.ru/topforecast/')
        self._driver.implicitly_wait(15)

        self._driver.find_element_by_class_name('button_default').click()
        sleep(2)

        try:
            select = Select(self._driver.find_element_by_id('sport'))
            select.select_by_value('2')
            sleep(1)
        except NoSuchElementException:
            return False, 'No tennis forecasts for today comeback later'

        self._driver.find_element_by_class_name('button_default').click()
        sleep(5)

        html = self._driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        tags = soup.find_all(class_='top-forecast__match-name')
        matches = [tag.find('a').get('href') for tag in tags][:limit]
        shuffle(matches)

        htmls = []
        for match in matches:
            self._driver.get(match)
            sleep(2)
            htmls.append(self._driver.page_source)

        self._driver.close()
        self._driver.quit()

        return htmls
