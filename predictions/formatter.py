# -*- coding: utf8 -*-

from googletrans import Translator


class Formatter:

    def __init__(self):
        '''
        Initialize Formatter by setting up googletrans Translator

        :return: returns nothing
        '''
        self._translator = Translator()

    @staticmethod
    def _raw_translated(text: str, src: str, dest: str):
        url = 'https://translate.google.com/?sl={}&tl={}&op=translate'
        gecko_path = r'C:\Users\khova\Desktop\Python\Code\TennisBetsPredictor\geckodriver.exe'
        from selenium import webdriver
        from time import sleep

        webdriver = webdriver.Firefox(executable_path=gecko_path)
        webdriver.get(url.format(src, dest))
        webdriver.implicitly_wait(15)
        text_area = webdriver.find_element_by_class_name('er8xn')

        for letter in text:
            text_area.send_keys(letter)
            sleep(0.08)

        sleep(5)

        translated = webdriver.find_element_by_xpath(
            '//*[@jsname="W297wb"]').text.strip()

        return translated

    def translate(self, text: str, src: str = 'ru', dest: str = 'en'):
        '''
        Translating given `str` text to dest language, English by default, from src language, Russiand by default

        :param text: Text to translate
        :param src: Source language to translate from
        :param dest: Destination language to translate to
        :return: returns translated `str` text in dest language
        '''
        try:
            r_text = self._translator.translate(text, src=src, dest=dest)
            return r_text.text
        except:
            print('Gonna use _raw_translated method')
            return self._raw_translated(text, src, dest)

    @staticmethod
    def format_(string):
        '''
        Format given `str` string by replacing Russian betting tips with appropriate English ones

        :param string: Betting tip to format
        :return: returns formatted `str`
        '''
        return string.replace('П', 'WINNER ').replace('ИТБ', 'Individual Total Over For Player#').replace('ИТМ', 'Individual Total Under For Player#').replace('ТБ', 'Total Over').replace('ТМ', 'Total Under').replace('Точный счет', 'Correct score').replace('ФОРА', 'Handicap').replace('по', 'by').replace('геймам', 'games').replace('сетам', 'sets')


if __name__ == '__main__':
    f = Formatter()

    translated = f.translate('Думаю сегодня выиграет Павлюченко в связи с её очень хорошей подготовкой к турниру в Праге и настрою. Помимо этого, на протяжении данного полугодия Павлюченко завоевала 3 титула и сумела выиграть 21 матч в ряд. Мой выбор за Россиянкой. Всем удачных ставок!!!')
    print(translated)

    formatted = f.format_('ИТБ2 10'), f.format_(
        'Точный счет 2:0'), f.format_('ТМ 21.5'), f.format_('П1')
    print(formatted)
