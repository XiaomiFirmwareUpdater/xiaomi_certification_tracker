import difflib
from datetime import date
from os import system, environ

from requests import post

# variables and tokens
today = str(date.today())
telegram_chat = "@XiaomiCertificationTracker"
try:
    bottoken = environ['bottoken']
    GIT_OAUTH_TOKEN = environ['XFU']
except KeyError:
    print("Key not found, skipping!")


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
        print("Telegram Message sent")
    else:
        print("Telegram Error")


def git_commit_push(file):
    system("git add data/{} && git -c \"user.name=XiaomiFirmwareUpdater\" "
           "-c \"user.email=xiaomifirmwareupdater@gmail.com\" commit -m \"[skip ci] {}: {}\" && "" \
       ""git push -q https://{}@github.com/XiaomiFirmwareUpdater/xiaomi_certification_tracker.git HEAD:master"
           .format(file, str(file).split(".")[0], today, GIT_OAUTH_TOKEN))
