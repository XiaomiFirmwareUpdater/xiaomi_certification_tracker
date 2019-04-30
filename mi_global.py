#!/usr/bin/env python3.7
"""mi.com scrapper that gets Xiaomi devices info"""

from os import rename, path
from bs4 import BeautifulSoup
from requests import get

import extra

# backup
if path.exists('data/mi_global.md'):
    rename('data/mi_global.md', 'data/mi_global_old.md')

# scrap
DATA = BeautifulSoup(
    get('https://www.mi.com/global/certification/compliance/').content, 'html.parser')\
    .findAll("div", {"class": "item"})
with open('data/mi_global.md', 'w') as o:
    o.write("# Xiaomi devices for Global market\n\n")
    for group in DATA:
        devices = group.findAll("a")
        for device in devices:
            o.write('- [' + device.text + '](https:' + device['href'] + ')\n')

# diff
extra.compare('data/mi_global_old.md', 'data/mi_global.md')

# post
with open('data/mi_global_changes.md', 'r') as c:
    for line in c:
        device = line.strip().split("- ")[1]
        telegram_message = "New Xiaomi device Added to Mi Global website! \n" \
                           "*Name:* {}".format(device)
        extra.tg_post(telegram_message)

# commit and push
extra.git_commit_push('mi_global.md')
