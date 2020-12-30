# -*- coding: utf8 -*-

from googletrans import Translator

translator = Translator()


def translate(text, src='ru', dest='en'):
    try:
        r_text = translator.translate(text, src=src, dest=dest)
        return r_text.text
    except:
        return raw_translated(text)


def raw_translated(text):
    from selenium import webdriver
    return text


def format_(string):
    return string.replace('П', 'WINNER ').replace('ИТБ', 'Individual Total Over For Player#').replace('ИТМ', 'Individual Total Under For Player#').replace('ТБ', 'Total Over').replace('ТМ', 'Total Under').replace('Точный счет', 'Correct score').replace('ФОРА', 'Handicap').replace('по', 'by').replace('геймам', 'games').replace('сетам', 'sets')
