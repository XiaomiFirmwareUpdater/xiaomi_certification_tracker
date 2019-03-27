import re
from os import rename, path

import extra
from bs4 import BeautifulSoup
from requests import get

# backup
if path.exists('data/fccid.md'):
    rename('data/fccid.md', 'data/fccid_old.md')

# scrap
fccid_data = BeautifulSoup(get('https://fccid.io/2AFZZ').content, 'html.parser').findAll("table", {"class": "table"})[1]
data = list(dict.fromkeys(fccid_data))[2:-1]
with open('data/fccid.md', 'w') as o:
    o.write("| FCC ID | Date | Certification |" + '\n')
    o.write("|---|---|---|" + '\n')
    for i in data:
        model = BeautifulSoup(str(i), 'html.parser').find('a').text
        date = re.findall(r"\d\d\d\d-\d\d-\d\d", BeautifulSoup(str(i), 'html.parser').findAll('td')[0].text)[0]
        o.write("|{0}|{1}|[Here](https://gov.fccid.io/{0})|\n".format(model, date))

# diff
extra.compare('data/fccid_old.md', 'data/fccid.md')

# post
with open('data/fccid_changes.md', 'r') as c:
    for line in c:
        data = line.split("|")
        model = data[1]
        date = data[2]
        link = data[3]
        telegram_message = "New FCCID Certificate passed! \n*Model:* `{}`\n*Date:* `{}`\n*Certification:* {}\n".format(model, date, link)
        extra.tg_post(telegram_message)

# commit and push
extra.git_commit_push('fccid.md')
