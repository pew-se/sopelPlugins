#!/usr/bin/python
# -*- coding: utf-8 -*-
# Module for sopel, will fetch coronavirus data
import re
from collections import defaultdict

from bs4 import BeautifulSoup
from sopel import module
import requests


class Corona:
    __deaths = 0
    __recovered = 0
    __confirmed = 0
    __critical = 0
    __new_deaths = ''
    __new_cases = ''

    @property
    def deaths(self):
        return self.__deaths

    @deaths.setter
    def deaths(self, value):
        self.__deaths += value

    @property
    def new_deaths(self):
        return self.__new_deaths

    @new_deaths.setter
    def new_deaths(self, value):
        self.__new_deaths += value

    @property
    def recovered(self):
        return self.__recovered

    @recovered.setter
    def recovered(self, value):
        self.__recovered += value

    @property
    def confirmed(self):
        return self.__confirmed

    @confirmed.setter
    def confirmed(self, value):
        self.__confirmed += value

    @property
    def new_cases(self):
        return self.__new_cases

    @new_cases.setter
    def new_cases(self, value):
        self.__new_cases += value

    @property
    def critical(self):
        return self.__critical

    @critical.setter
    def critical(self, value):
        self.__critical += value


@module.commands('corona', 'cor')
def coronavirus(bot, trigger):
    if trigger.group(2) is None:
        country = 'World'.lower()
    else:
        country = trigger.group(2).lower()

    base_url = 'https://www.worldometers.info/coronavirus/'
    response = requests.get(base_url)
    if not response.status_code == 200:
        return None

    content = response.content
    if not content:
        return None

    soup = BeautifulSoup(response.content.decode(), "html.parser")
    cases = defaultdict(Corona)

    table = soup.find('table', {'id': 'main_table_countries_today'}).find("tbody", recursive=True)
    rows = table.find_all('tr')

    tag_re = re.compile(r'(<!--.*?-->|<[^>]*>)')
    total = Corona
    for row in rows:
        try:
            columns = row.find_all('td')
            columns = [tag_re.sub('', str(x)).strip() for x in columns]
            columns[0] = columns[1].lower()
            if columns[1].lower() == 'total:':
                total.deaths = int(columns[4].replace(',', '') or 0)
                total.confirmed = int(columns[2].replace(',', '') or 0)
                total.new_deaths = str(columns[5])
                total.new_cases = str(columns[3])
                total.critical = int(columns[9].replace(',', '') or 0)
                continue
            cases[columns[0].lower()].deaths = int(columns[4].replace(',', '') or 0)
            cases[columns[0].lower()].confirmed = int(columns[2].replace(',', '') or 0)
            cases[columns[0].lower()].new_deaths = str(columns[5])
            cases[columns[0].lower()].new_cases = str(columns[3])
            cases[columns[0].lower()].critical = int(columns[9].replace(',', '') or 0)
        except:
            continue
        if columns[1] == country:
            break


    if str(country) in cases:
        bot.say(f'😷 {cases[str(country)].confirmed}'
                f'({cases[str(country)].new_cases}) '
                f'😵 {cases[str(country)].critical} '
                f'⚰️ {cases[str(country)].deaths}'
                f'({cases[str(country)].new_deaths}) '
                f'☠️ {round(cases[str(country)].deaths / cases[str(country)].confirmed * 100, 2)}%\x03 ')
    else:
        bot.say(f'Country not in the list')

