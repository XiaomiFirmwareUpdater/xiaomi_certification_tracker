#!/usr/bin/env python3.7
"""fccid.io scrapper that gets Xiaomi devices info"""

from os import rename, path
from bs4 import BeautifulSoup
from requests import get

import extra

# backup
if path.exists('data/tenaa_mobile.md'):
    rename('data/tenaa_mobile.md', 'data/tenaa_mobile_old.md')

MI_DATA = BeautifulSoup(
    get('http://shouji.tenaa.com.cn/Mobile/mobileindex_MHSS.aspx' +
        '?code=ppRNoBcXhFGdKI3DQ%2fot0g%3d%3d').content,
    'html.parser').findAll("table", {"class": "lineGrayTD"})
REDMI_DATA = BeautifulSoup(
    get('http://shouji.tenaa.com.cn/Mobile/mobileindex_MHSS.aspx' +
        '?code=ppRNoBcXhFHQLiUSN5abWg%3D%3D').content,
    'html.parser').findAll("table", {"class": "lineGrayTD"})
with open('data/tenaa_mobile.md', 'w', encoding='utf-8') as o:
    o.write("# Xiaomi devices listed in TENAA Mobile website\n\n")
    for table in MI_DATA + REDMI_DATA:
        for row in table.findAll('tr'):
            for cell in row.findAll('td', {"style": "height:15px;"}):
                if "M" in cell.text:
                    o.write('- [' + cell.a.text.replace("Ð¡Ã×", "MI ") +
                            '](http://shouji.tenaa.com.cn/Mobile/' + cell.a['href'] + ')\n')

# diff
extra.compare('data/tenaa_mobile_old.md', 'data/tenaa_mobile.md')

# post
with open('data/tenaa_mobile_changes.md', 'r') as c:
    for line in c:
        device = line.strip().split("- ")[1]
        telegram_message = "New Xiaomi device added to TENAA mobile website! \n" \
                           "*Name:* {}".format(device)
        extra.tg_post(telegram_message)

# commit and push
extra.git_commit_push('tenaa_mobile.md')
