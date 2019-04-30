#!/usr/bin/env python3.7
"""common functions used in scrapping scripts"""

import difflib
from datetime import date
from os import system, environ

from requests import post

# variables and tokens
TODAY = str(date.today())
TELEGRAM_CHAT = "@XiaomiCertificationTracker"
try:
    BOTTOKEN = environ['bottoken']
    GIT_OAUTH_TOKEN = environ['XFU']
except KeyError:
    print("Key not found, skipping!")


def compare(old, new):
    """compare two files line by line and write additions to new file"""
    with open(old, 'r') as old_, open(new, 'r') as new_:
        old_data = old_.readlines()
        new_data = new_.readlines()
    diff = difflib.unified_diff(old_data, new_data, fromfile=old, tofile=new)
    changes = []
    for line in diff:
        if line.startswith('+'):
            changes.append(str(line))
    out = ''.join(changes[1:]).replace("+", "")
    with open(str(new).split(".")[0] + '_changes.md', 'w') as output:
        output.write(out)


def tg_post(message):
    """send message to telegram"""
    params = (
        ('chat_id', TELEGRAM_CHAT),
        ('text', message),
        ('parse_mode', "Markdown"),
        ('disable_web_page_preview', "yes")
    )
    telegram_url = "https://api.telegram.org/bot" + BOTTOKEN + "/sendMessage"
    telegram_req = post(telegram_url, params=params)
    telegram_status = telegram_req.status_code
    if telegram_status == 200:
        print("Telegram Message sent")
    else:
        print("Telegram Error")


def git_commit_push(file):
    """commit changes and push to github"""
    system("git add data/{} && git -c \"user.name=XiaomiFirmwareUpdater\" "
           "-c \"user.email=xiaomifirmwareupdater@gmail.com\" commit -m \"[skip ci] {}: {}\" && "" \
       ""git push -q https://{}@github.com/XiaomiFirmwareUpdater/"
           "xiaomi_certification_tracker.git HEAD:master"
           .format(file, str(file).split(".")[0], TODAY, GIT_OAUTH_TOKEN))
