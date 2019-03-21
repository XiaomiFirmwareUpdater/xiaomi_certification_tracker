import difflib
from datetime import date
from os import environ, rename, path, system

from bs4 import BeautifulSoup
from requests import get, post

# variables and tokens
today = str(date.today())
telegram_chat = "@XiaomiCertificationTracker"
bottoken = environ['bottoken']
GIT_OAUTH_TOKEN = environ['XFU']

# backup
if path.exists('README.md'):
    rename('README.md', 'README_old.md')

# scrap
mi_data = BeautifulSoup(get('http://shouji.tenaa.com.cn/Mobile/mobileindex_MHSS.aspx?code=ppRNoBcXhFGdKI3DQ%2fot0g%3d%3d').content, 'html.parser').findAll("table", {"class": "lineGrayTD"})
redmi_data = BeautifulSoup(get('http://shouji.tenaa.com.cn/Mobile/mobileindex_MHSS.aspx?code=ppRNoBcXhFHQLiUSN5abWg%3D%3D').content, 'html.parser').findAll("table", {"class": "lineGrayTD"})
data = BeautifulSoup(get('https://wap.tenaa.com.cn/WSFW/CertQueryResult.aspx?code=oJngJpdSu3KUvOjY51HvUAsAMbCrr8GOTsbUizvfWU0A2eyUmxgmLkHXNlFWiwVwJDHWdOzREVMtXycWOsHGUbDYTXGDdhs0gmJ%2FqMQjeNjCwczFyX3zDg%3D%3D').content, 'html.parser').findAll("table")[2]

with open('README.md', 'w') as o:
    o.write("| Model | License | Photos | Info |" + '\n')
    o.write("|---|---|---|---|" + '\n')
    for row in data.find_all('tr')[2:-1]:
        for cell in row.find_all('td'):
            if cell.a:
                try:
                    o.write("|[Here](https://wap.tenaa.com.cn/WSFW/" + cell.a['href'] + ")")
                except KeyError:
                    o.write("|" + str(cell.text).strip())
            else:
                o.write("|" + str(cell.text).strip())
        o.write("|" + '\n')

# diff
with open('README_old.md', 'r') as old, open('README.md', 'r') as new:
    o = old.readlines()
    n = new.readlines()
diff = difflib.unified_diff(o, n, fromfile='README_old.md', tofile='README.md')
changes = []
for line in diff:
    if line.startswith('+'):
        changes.append(str(line))
new = ''.join(changes[1:]).replace("+", "")
with open('README_changes.md', 'w') as o:
    o.write(new)

# post
with open('README_changes.md', 'r') as c:
    for line in c:
        info = line.split("|")
        model = info[1]
        license = info[2]
        photos = info[3]
        info = info[4]
        for table in mi_data:
            for row in table.find_all('tr'):
                for cell in row.find_all('td'):
                    if model in cell.text:
                        details = "http://shouji.tenaa.com.cn/Mobile/" + cell.a['href']
        for table in redmi_data:
            for row in table.find_all('tr'):
                for cell in row.find_all('td'):
                    if model in cell.text:
                        details = "http://shouji.tenaa.com.cn/Mobile/" + cell.a['href']
        telegram_message = "New Certificate detected! \n*Device Model:* `{}`\n*License:* {}\n*Info:* {}\n" \
                           "*Photos:* {}\n*Details:* [Here]({})\n".format(model, license, info, photos, details)
        params = (
            ('chat_id', telegram_chat),
            ('text', telegram_message),
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

# commit and push
system("git add README.md && git -c \"user.name=XiaomiFirmwareUpdater\" "
       "-c \"user.email=xiaomifirmwareupdater@gmail.com\" commit -m \"[skip ci] sync: {}\" && "" \
   ""git push -q https://{}@github.com/XiaomiFirmwareUpdater/xiaomi_certification_tracker.git HEAD:master"
       .format(today, GIT_OAUTH_TOKEN))
