#!/usr/bin/env python3.7
"""Merge output files into one table"""

import extra

# Initialize
TABLES = ['fccid', 'nbtc', 'tenaa_cert', 'tkdn', 'wifi']
TABLES_DATA = []
COMPARE = []
MODELS = []
NAMES = {'M1810E5E': 'MI MIX 3', 'M1806D9E': 'MI Pad 4',
         'M1806D9PE': 'MI Pad 4 Plus', 'M1901F7BE': 'Redmi Note 7',
         'M1901F9E': 'MI Play', 'M1901F9T': 'MI Play'}
# Load data
for file in TABLES:
    with open('data/' + file + '.md', 'r') as i:
        file = i.readlines()
        TABLES_DATA.append(file)
for i in TABLES_DATA[4][2:]:
    MODELS.append(i.split('|')[2])  # load models from wifi data
for i in TABLES_DATA[2][2:]:
    MODELS.append(i.split('|')[1])  # load models from tenaa cert data
for i in TABLES_DATA[4][2:]:
    NAMES.update({i.split('|')[2]: i.split('|')[1]})  # load devices names as dict

# Search models:
for model in MODELS:
    if model.startswith("M"):
        name = ''
        try:
            name = next(v for k, v in NAMES.items() if model[:-1] in k)
        except StopIteration:
            pass
        ffcid_model = model[-3:]  # last three letters of model (F2G)
        if any(ffcid_model in s for s in TABLES_DATA[0][2:]):  # search fccid data
            fccid = '✓'
        else:
            fccid = '✗'
        if any(model in s for s in TABLES_DATA[1][2:]):  # search nbtc data
            nbtc = '✓'
        else:
            nbtc = '✗'
        if any(model in s for s in TABLES_DATA[2][2:]):  # search tenaa_cert data
            tenaa_cert = '✓'
        else:
            tenaa_cert = '✗'
        if any(model in s for s in TABLES_DATA[3][2:]):  # search tkdn data
            tkdn = '✓'
        else:
            tkdn = '✗'
        if any(model in s for s in TABLES_DATA[4][2:]):  # search wifi data
            wifi = '✓'
        else:
            wifi = '✗'
        COMPARE.append('|{}|{}|{}|{}|{}|{}|{}|'
                       .format(name, model, fccid, nbtc, tenaa_cert, tkdn, wifi))

# Write the table
DATA = list(dict.fromkeys(COMPARE))  # remove duplicates
with open('data/aio.md', 'w') as o:
    o.write('| Name | Model | [FCCID]'
            '(https://github.com/XiaomiFirmwareUpdater/xiaomi_certification_tracker/'
            'blob/master/data/fccid.md) | '
            '[Thailand NBTC](https://github.com/XiaomiFirmwareUpdater/xiaomi_certification_tracker/'
            'blob/master/data/nbtc.md) | [Chinese TENAA](https://github.com/XiaomiFirmwareUpdater/'
            'xiaomi_certification_tracker/blob/master/data/tenaa_mobile.md) | '
            '[Indonesian TKDN](https://github.com/XiaomiFirmwareUpdater/'
            'xiaomi_certification_tracker/blob/master/data/tkdn.md) | '
            '[Wi-Fi Alliance](https://github.com/XiaomiFirmwareUpdater/'
            'xiaomi_certification_tracker/blob/master/data/wifi.md)  |\n')
    o.write('|---|---|---|---|---|---|---|\n')
    for line in DATA:
        o.write(line + '\n')

# Commit and Push
extra.git_commit_push('aio.md')
