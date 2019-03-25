from os import rename, path

from bs4 import BeautifulSoup
import extra
from requests import get

# backup
if path.exists('data/tenaa.md'):
    rename('data/tenaa.md', 'data/tenaa_old.md')

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

with open('data/tmp.md', 'w') as o:
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

with open('data/tenaa.md', 'w') as o, open('data/tmp.md', 'r') as i:
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
extra.compare('data/tenaa_old.md', 'data/tenaa.md')

# post
with open('data/tenaa_changes.md', 'r') as c:
    for line in c:
        data = line.split("|")
        model = data[1]
        license = data[2]
        photos = data[3]
        info = data[4]
        details = data[5]
        telegram_message = "New TENAA Certificate detected! \n*Model:* `{}`\n*License:* {}\n*Info:* {}\n" \
                           "*Photos:* {}\n*Details:* {}\n".format(model, license, info, photos, details)
        extra.tg_post(telegram_message)

# commit and push
extra.git_commit_push('tenaa.md')
