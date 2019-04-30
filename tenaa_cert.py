#!/usr/bin/env python3.7
"""wap.tenaa.com.cn scrapper that gets Xiaomi devices info"""

from os import rename, path
from bs4 import BeautifulSoup
from requests import get

import extra

# backup
if path.exists('data/tenaa_cert.md'):
    rename('data/tenaa_cert.md', 'data/tenaa_cert_old.md')

# scrap
DATA = BeautifulSoup(get(
    'https://wap.tenaa.com.cn/WSFW/CertQueryResult.aspx?' +
    'code=oJngJpdSu3KUvOjY51HvUAsAMbCrr8GOTsbUizvfWU0A2eyUmxgmLkHXNlFWiwVwJ' +
    'DHWdOzREVMtXycWOsHGUbDYTXGDdhs0gmJ%2FqMQjeNjCwczFyX3zDg%3D%3D').content,
                     'html.parser').findAll("table")[2]

with open('data/tmp.md', 'w') as o:
    for row in DATA.find_all('tr')[2:-1]:
        for cell in row.find_all('td'):
            if cell.a:
                try:
                    o.write("|[Here](https://wap.tenaa.com.cn/WSFW/" + cell.a['href'] + ")")
                except KeyError:
                    o.write("|" + str(cell.text).strip())
            else:
                o.write("|" + str(cell.text).strip())
        o.write("|" + '\n')

# sort
with open('data/tenaa_cert.md', 'w') as o, open('data/tmp.md', 'r') as i:
    DATA = sorted(i.readlines(), reverse=True)
    o.write("| Model | License | Photos | Info |" + '\n')
    o.write("|---|---|---|---|" + '\n')
    for item in DATA:
        o.write(item)

# diff
extra.compare('data/tenaa_cert_old.md', 'data/tenaa_cert.md')

# post
with open('data/tenaa_cert_changes.md', 'r') as c:
    for line in c:
        data = line.split("|")
        model = data[1]
        license_ = data[2]
        photos = data[3]
        info = data[4]
        telegram_message = "New TENAA Certificate detected! \n" \
                           "*Model:* `{}`\n" \
                           "*License:* {}\n" \
                           "*Info:* {}\n" \
                           "*Photos:* {}\n".format(model, license_, info, photos)
        extra.tg_post(telegram_message)

# commit and push
extra.git_commit_push('tenaa_cert.md')
