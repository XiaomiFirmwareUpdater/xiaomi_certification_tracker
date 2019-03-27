from os import rename, path

from bs4 import BeautifulSoup
import extra
from requests import get

# backup
if path.exists('data/nbtc.md'):
    rename('data/nbtc.md', 'data/nbtc_old.md')

# scrap
nbtc_data = BeautifulSoup(
    get(
        'http://mocheck.nbtc.go.th/search?keyword=Xiaomi&pageLimit=150').content,
    'html.parser').find("div", {"class": "row item-blocks-connected"}).findAll("div", {"class": "row"})[1:]
with open('data/nbtc.md', 'w') as o:
    o.write("| Brand | Product | Model | Certificate |" + '\n')
    o.write("|---|---|---|---|" + '\n')
    for i in nbtc_data:
        data = i.find("a")
        if data:
            brand = data.findAll("div", {"class": "col-xs-12 col-md-2 text-left"})[0].text
            product = ''
            try:
                product = data.findAll("div", {"class": "col-xs-12 col-md-2 text-left"})[1].text.split("(")[1].split(")")[0]
            except IndexError:
                pass
            model = data.findAll("div", {"class": "col-xs-12 col-md-2 text-left"})[1].text.split(" ")[0]
            certificate = data.find("div", {"class": "col-xs-12 col-md-2 text-center"}).text.strip()
            link = data['href']
            o.write("|{}|{}|{}|[{}]({})|".format(brand, product, model, certificate, link) + '\n')

# diff
extra.compare('data/nbtc_old.md', 'data/nbtc.md')

# post
with open('data/nbtc_changes.md', 'r') as c:
    for line in c:
        data = line.split("|")
        brand = data[1]
        product = data[2]
        model = data[3]
        certificate = data[4]
        telegram_message = "New Thailand NBTC Certificate for {} device detected! \n*Name:* `{}`\n*Model:* `{}`\n" \
                           "*Certification:* {}\n".format(brand, product, model, certificate)
        extra.tg_post(telegram_message)

# commit and push
extra.git_commit_push('nbtc.md')
