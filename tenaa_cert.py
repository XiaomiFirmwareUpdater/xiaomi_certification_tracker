from os import rename, path

from bs4 import BeautifulSoup
import extra
from requests import get

# backup
if path.exists('data/tenaa_cert.md'):
    rename('data/tenaa_cert.md', 'data/tenaa_cert_old.md')

# scrap
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

# sort
with open('data/tenaa_cert.md', 'w') as o, open('data/tmp.md', 'r') as i:
    sorted_data = sorted(i.readlines(), reverse=True)
    o.write("| Model | License | Photos | Info |" + '\n')
    o.write("|---|---|---|---|" + '\n')
    for item in sorted_data:
        o.write(item)

# diff
extra.compare('data/tenaa_cert_old.md', 'data/tenaa_cert.md')

# post
with open('data/tenaa_cert_changes.md', 'r') as c:
    for line in c:
        data = line.split("|")
        model = data[1]
        license = data[2]
        photos = data[3]
        info = data[4]
        telegram_message = "New TENAA Certificate detected! \n*Model:* `{}`\n*License:* {}\n*Info:* {}\n" \
                           "*Photos:* {}\n".format(model, license, info, photos)
        extra.tg_post(telegram_message)

# commit and push
extra.git_commit_push('tenaa_cert.md')
