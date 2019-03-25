from os import rename, path

import extra
from bs4 import BeautifulSoup
from requests import get

# backup
if path.exists('data/mi_india.md'):
    rename('data/mi_india.md', 'data/mi_india_old.md')

# scrap
mi_india_data = BeautifulSoup(
    get('https://www.mi.com/in/certification/rfexposure/').content, 'html.parser').findAll("div", {
    "class": "item"})
with open('data/mi_india.md', 'w') as o:
    o.write("# Xiaomi devices for Indian market\n\n")
    for group in mi_india_data:
        devices = group.findAll("p")
        for device in devices:
            o.write('- ' + device.text + '\n')

# diff
extra.compare('data/mi_india_old.md', 'data/mi_india.md')

# post
with open('data/mi_india_changes.md', 'r') as c:
    for line in c:
        device = line.strip().split("- ")[1]
        telegram_message = "New Xiaomi device Added to Mi India website! \n*Name:* `{}`".format(device)
        extra.tg_post(telegram_message)

# commit and push
extra.git_commit_push('data/mi_global.md')
