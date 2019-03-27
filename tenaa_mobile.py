from os import rename, path

from bs4 import BeautifulSoup
import extra
from requests import get

# backup
if path.exists('data/tenaa_mobile.md'):
    rename('data/tenaa_mobile.md', 'data/tenaa_mobile_old.md')

mi_data = BeautifulSoup(
    get('http://shouji.tenaa.com.cn/Mobile/mobileindex_MHSS.aspx?code=ppRNoBcXhFGdKI3DQ%2fot0g%3d%3d').content,
    'html.parser').findAll("table", {"class": "lineGrayTD"})
redmi_data = BeautifulSoup(
    get('http://shouji.tenaa.com.cn/Mobile/mobileindex_MHSS.aspx?code=ppRNoBcXhFHQLiUSN5abWg%3D%3D').content,
    'html.parser').findAll("table", {"class": "lineGrayTD"})
with open('data/tenaa_mobile.md', 'w', encoding='utf-8') as o:
    o.write("# Xiaomi devices listed in TENAA Mobile website\n\n")
    for table in mi_data + redmi_data:
        for row in table.findAll('tr'):
            for cell in row.findAll('td', {"style": "height:15px;"}):
                if "M" in cell.text:
                    o.write('- [' + cell.a.text.replace("Ð¡Ã×", "MI ") + '](https://' + cell.a['href'] + ')\n')

# diff
extra.compare('data/tenaa_mobile_old.md', 'data/tenaa_mobile.md')

# post
with open('data/tenaa_mobile_changes.md', 'r') as c:
    for line in c:
        device = line.strip().split("- ")[1]
        telegram_message = "New Xiaomi device added to TENAA mobile website! \n*Name:* {}".format(device)
        extra.tg_post(telegram_message)

# commit and push
extra.git_commit_push('tenaa_mobile.md')
