import extra

# Initialize
tables = ['fccid', 'nbtc', 'tenaa_cert', 'tkdn', 'wifi']
tables_data = []
compare = []
models = []
names = {'M1810E5E': 'MI MIX 3', 'M1806D9E': 'MI Pad 4', 'M1806D9PE': 'MI Pad 4 Plus', 'M1901F7BE': 'Redmi Note 7',
         'M1901F9E': 'MI Play', 'M1901F9T': 'MI Play'}
# Load data
for file in tables:
    with open('data/' + file + '.md', 'r') as i:
        file = i.readlines()
        tables_data.append(file)
for i in tables_data[4][2:]:
    models.append(i.split('|')[2])  # load models from wifi data
for i in tables_data[2][2:]:
    models.append(i.split('|')[1])  # load models from tenaa cert data
for i in tables_data[4][2:]:
    names.update({i.split('|')[2]: i.split('|')[1]})  # load devices names as dict

# Search models:
for model in models:
    if model.startswith("M"):
        name = ''
        try:
            name = next(v for k, v in names.items() if model[:-1] in k)
        except StopIteration:
            pass
        ffcid_model = model[-3:]  # last three letters of model (F2G)
        if any(ffcid_model in s for s in tables_data[0][2:]):  # search fccid data
            fccid = '✓'
        else:
            fccid = '✗'
        if any(model in s for s in tables_data[1][2:]):  # search nbtc data
            nbtc = '✓'
        else:
            nbtc = '✗'
        if any(model in s for s in tables_data[2][2:]):  # search tenaa_cert data
            tenaa_cert = '✓'
        else:
            tenaa_cert = '✗'
        if any(model in s for s in tables_data[3][2:]):  # search tkdn data
            tkdn = '✓'
        else:
            tkdn = '✗'
        if any(model in s for s in tables_data[4][2:]):  # search wifi data
            wifi = '✓'
        else:
            wifi = '✗'
        compare.append('|{}|{}|{}|{}|{}|{}|{}|'.format(name, model, fccid, nbtc, tenaa_cert, tkdn, wifi))

# Write the table
data = list(dict.fromkeys(compare))  # remove duplicates
with open('data/aio.md', 'w') as o:
    o.write('| Name | Model | [FCCID](https://github.com/XiaomiFirmwareUpdater/xiaomi_certification_tracker/blob/master/data/fccid.md) | [Thailand NBTC](https://github.com/XiaomiFirmwareUpdater/xiaomi_certification_tracker/blob/master/data/nbtc.md) | [Chinese TENAA](https://github.com/XiaomiFirmwareUpdater/xiaomi_certification_tracker/blob/master/data/tenaa_cert.md) | [Indonesian TKDN](https://github.com/XiaomiFirmwareUpdater/xiaomi_certification_tracker/blob/master/data/tkdn.md) | [Wi-Fi Alliance](https://github.com/XiaomiFirmwareUpdater/xiaomi_certification_tracker/blob/master/data/wifi.md)  |\n')
    o.write('|---|---|---|---|---|---|---|\n')
    for line in data:
        o.write(line + '\n')

# Commit and Push
extra.git_commit_push('aio.md')
