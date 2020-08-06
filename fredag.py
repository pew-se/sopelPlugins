from sopel import module
from bs4 import BeautifulSoup
import requests
import re


@module.rule('Är det fredag')
def isItFriday(bot, trigger):
    base_url = 'https://ärdetfredag.se/'
    response = requests.get(base_url)
    if not response.status_code == 200:
        return None

    content = response.content
    if not content:
        return None

    soup = BeautifulSoup(response.content.decode(), "html.parser")
    raw = soup.find('div', {'id': 'content'})

    answer_re = re.compile(r'(.*<span>|</span>.*)')
    answer = answer_re.sub('', str(raw)).strip()

    bot.say(f'{answer}')