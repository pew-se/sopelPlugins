from sopel import module
from bs4 import BeautifulSoup
import requests
import re

@module.commands('middag', 'm')
def dinner(bot, trigger):
    if trigger.group(2) == 'veg':
        base_url = 'https://vadfanskajaglagatillmiddag.nu/vegetariskt'
    else:
        base_url = 'https://vadfanskajaglagatillmiddag.nu/'

    response = requests.get(base_url)
    if not response.status_code == 200:
        return None

    content = response.content
    if not content:
        return None

    soup = BeautifulSoup(response.content.decode(), "html.parser")
    raw = soup.find('a', {'rel': 'noopener noreferrer'})

    meal_re = re.compile(r'(<!--.*?-->|<[^>]*>)')
    mealName = meal_re.sub('', str(raw)).strip()
    link_re = re.compile(r'(<a href="|" .*)')
    mealLink = link_re.sub('', str(raw)).strip()

    bot.say(f'Du kan väl för fan laga lite {mealName}: {mealLink}')
