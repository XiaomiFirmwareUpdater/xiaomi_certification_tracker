import difflib
from datetime import date
from os import environ, rename, path, system

from bs4 import BeautifulSoup
from requests import get, post


def compare(old, new):
    with open(old, 'r') as o, open(new, 'r') as n:
        old_data = o.readlines()
        new_data = n.readlines()
    diff = difflib.unified_diff(old_data, new_data, fromfile=old, tofile=new)
    changes = []
    for line in diff:
        if line.startswith('+'):
            changes.append(str(line))
    out = ''.join(changes[1:]).replace("+", "")
    with open(str(new).split(".")[0] + '_changes.md', 'w') as o:
        o.write(out)


def tg_post(message):
    params = (
        ('chat_id', telegram_chat),
        ('text', message),
        ('parse_mode', "Markdown"),
        ('disable_web_page_preview', "yes")
    )
    telegram_url = "https://api.telegram.org/bot" + bottoken + "/sendMessage"
    telegram_req = post(telegram_url, params=params)
    telegram_status = telegram_req.status_code
    if telegram_status == 200:
        print("{0}: Telegram Message sent".format(model))
    else:
        print("Telegram Error")


def git_commit(file):
    system("git add {} && git -c \"user.name=XiaomiFirmwareUpdater\" "
           "-c \"user.email=xiaomifirmwareupdater@gmail.com\" commit -m \"[skip ci] {}: {}\" && "" \
       ""git push -q https://{}@github.com/XiaomiFirmwareUpdater/xiaomi_certification_tracker.git HEAD:master"
           .format(file, str(file).split(".")[0], today, GIT_OAUTH_TOKEN))


# variables and tokens
today = str(date.today())
telegram_chat = "@XiaomiCertificationTracker"
bottoken = environ['bottoken']
GIT_OAUTH_TOKEN = environ['XFU']

# backup
if path.exists('tenaa.md'):
    rename('tenaa.md', 'tenaa_old.md')

# scrap
mi_data = BeautifulSoup(
    get('http://shouji.tenaa.com.cn/Mobile/mobileindex_MHSS.aspx?code=ppRNoBcXhFGdKI3DQ%2fot0g%3d%3d').content,
    'html.parser').findAll("table", {"class": "lineGrayTD"})
redmi_data = BeautifulSoup(
    get('http://shouji.tenaa.com.cn/Mobile/mobileindex_MHSS.aspx?code=ppRNoBcXhFHQLiUSN5abWg%3D%3D').content,
    'html.parser').findAll("table", {"class": "lineGrayTD"})
cert_data = BeautifulSoup(get(
    'https://wap.tenaa.com.cn/WSFW/CertQueryResult.aspx?code=oJngJpdSu3KUvOjY51HvUAsAMbCrr8GOTsbUizvfWU0A2eyUmxgmLkHXNlFWiwVwJDHWdOzREVMtXycWOsHGUbDYTXGDdhs0gmJ%2FqMQjeNjCwczFyX3zDg%3D%3D').content,
                          'html.parser').findAll("table")[2]

with open('data.md', 'w') as o:
    for row in cert_data.find_all('tr')[2:-1]:
        for cell in row.find_all('td'):
            if cell.a:
                try:
                    o.write("|[Here](https://wap.tenaa.com.cn/WSFW/" + cell.a['href'] + ")")
                except KeyError:
                    o.write("|" + str(cell.text).strip())
            else:
                o.write("|" + str(cell.text).strip())
        o.write("|" + '\n')

with open('tenaa.md', 'w') as o, open('data.md', 'r') as i:
    o.write("| Model | License | Photos | Info | Details |" + '\n')
    o.write("|---|---|---|---|---|" + '\n')
    for line in i:
        model = line.split("|")[1]
        try:
            for table in mi_data:
                for row in table.find_all('tr'):
                    for cell in row.find_all('td'):
                        if model in cell.text:
                            details = "http://shouji.tenaa.com.cn/Mobile/" + cell.a['href']
        except KeyError:
            o.write("|")
        try:
            for table in redmi_data:
                for row in table.find_all('tr'):
                    for cell in row.find_all('td'):
                        if model in cell.text:
                            details = "http://shouji.tenaa.com.cn/Mobile/" + cell.a['href']
        except KeyError:
            o.write("|")
        o.write(line.strip() + '[Here]({})|\n'.format(details))

# diff
compare('tenaa_old.md', 'tenaa.md')

# post
with open('tenaa_changes.md', 'r') as c:
    for line in c:
        data = line.split("|")
        model = data[1]
        license = data[2]
        photos = data[3]
        info = data[4]
        details = data[5]
        telegram_message = "New TENAA Certificate detected! \n*Model:* `{}`\n*License:* {}\n*Info:* {}\n" \
                           "*Photos:* {}\n*Details:* {}\n".format(model, license, info, photos, details)
        tg_post(telegram_message)
git_commit('tenaa.md')

# Wi-Fi scrapper
if path.exists('wifi.md'):
    rename('wifi.md', 'wifi_old.md')
wifi_data = BeautifulSoup(
    get('https://www.wi-fi.org/product-finder-results?sort_by=certified&sort_order=desc&keywords=Xiaomi').content,
    'html.parser').find("ul", {"class": "result-list"}).findAll("li")
with open('README.md', 'w') as o:
    o.write("| Product | Model | Type | Date | Certification |" + '\n')
    o.write("|---|---|---|---|---|" + '\n')
    for i in wifi_data:
        product = i.find("div", {"class": "details"}).findAll("span")[0]['title']
        model = i.find("div", {"class": "details"}).findAll("span")[1]['title']
        type = i.find("div", {"class": "details"}).findAll("span")[3]['title']
        date = i.find("div", {"class": "details"}).findAll("span")[4]['title']
        link = i.find("a", {"class": "download-cert"})['href']
        o.write("|{}|{}|{}|{}|[Here]({})|".format(product, model, type, date, link) + '\n')
compare('wifi_old.md', 'wifi.md')
with open('wifi_changes.md', 'r') as c:
    for line in c:
        data = line.split("|")
        product = data[1]
        model = data[2]
        type = data[3]
        date = data[4]
        link = data[5]
        telegram_message = "New Wi-Fi Certificate detected! \n*Name:* `{}`\n*Model:* `{}`\n*Type:* `{}`\n" \
                           "*Date:* `{}`\n*Certification:* {}\n".format(product, model, type, date, link)
        tg_post(telegram_message)
git_commit('wifi.md')
