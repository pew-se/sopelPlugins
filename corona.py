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
    __confirmed = 0
    __critical = 0
    __population = 0
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

    @property
    def population(self):
        return self.__population

    @population.setter
    def population(self, value):
        self.__population += value


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
    for row in rows:
        try:
            columns = row.find_all('td')
            columns = [tag_re.sub('', str(x)).strip() for x in columns]
            if columns[1].lower() == country:
                cases[country].deaths = int(columns[4].replace(',', '') or 0)
                cases[country].new_deaths = str(columns[5])
                cases[country].confirmed = int(columns[2].replace(',', '') or 0)
                cases[country].new_cases = str(columns[3])
                cases[country].critical = int(columns[9].replace(',', '') or 0)
                cases[country].population = int(columns[14].replace(',', '') or 0)
                break
        except:
            continue

    if str(country) in cases:
        bot.say(f'{country.capitalize()}: '
                f'😷 {cases[str(country)].confirmed}'
                f'({cases[str(country)].new_cases}) '
                f'😵 {cases[str(country)].critical}  '
                f'⚰️ {cases[str(country)].deaths}'
                f'({cases[str(country)].new_deaths}) '
                f'☠️ {round(cases[str(country)].deaths / cases[str(country)].confirmed * 100, 2)}% of cases, '
                f'{round(cases[str(country)].deaths / cases[str(country)].population * 100, 2)}% of population')
    else:
        bot.say(f'{country.capitalize()} is not in the list')

