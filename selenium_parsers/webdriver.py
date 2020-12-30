from selenium import webdriver


URL = 'https://matchstat.com/tennis/all-upcoming-matches'


class Webdriver:
    def __init__(self):
        self._driver = webdriver.Firefox(service_log_path='NUL')
        self._driver.maximize_window()

    def kill(self):
        self._driver.close()
        self._driver.quit()