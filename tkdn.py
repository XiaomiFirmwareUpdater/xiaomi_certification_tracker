from os import rename, path

import extra
from bs4 import BeautifulSoup
from requests import get

# backup
if path.exists('data/tkdn.md'):
    rename('data/tkdn.md', 'data/tkdn_old.md')

# scrap
links_list = BeautifulSoup(
    get('http://tkdn.kemenperin.go.id/sertifikat_perush.php?id=u3XRjsixJLDGlwf0VRZb2q9VjYsbJZJ7T8GXTnJIcVI').content,
    'html.parser').find("table", {"class": "table table-hover"}).findAll("a")
links = []
for i in links_list:
    links.append("http://tkdn.kemenperin.go.id/" + i['href'])
with open('data/tkdn.md', 'w') as o:
    o.write("| Model | Certificate | Reference Number | Date |" + '\n')
    o.write("|---|---|---|---|" + '\n')
    for link in links:
        data = BeautifulSoup(get(link).content, 'html.parser')
        model = data.findAll("table")[1].findAll('td')[5].text
        if model.startswith("MI"):
            cert = data.findAll("table")[0].findAll('td')[6].text
            date = data.findAll("table")[0].findAll('td')[9].text
            ref = data.findAll("table")[0].findAll('td')[15].text
            o.write("|{}|[{}]({})|{}|{}|\n".format(model, cert, link, ref, date))

# diff
extra.compare('data/tkdn_old.md', 'data/tkdn.md')

# post
with open('data/tkdn_changes.md', 'r') as c:
    for line in c:
        data = line.split("|")
        model = data[1]
        cert = data[2]
        ref = data[3]
        date = data[4]
        telegram_message = "New TKDN Certificate detected! \n*Model:* `{}`\n*Certification:* {}\n" \
                           "*Reference Number:* `{}`\n*Date:* `{}`\n".format(model, cert, ref, date)
        extra.tg_post(telegram_message)

# commit and push
extra.git_commit_push('tkdn.md')
