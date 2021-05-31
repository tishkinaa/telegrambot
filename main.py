
url = "https://api.pik.ru/v1/bulk/chessplan?new=1&block_id=241&types=1,2"
# url = "https://api.pik.ru/v1/bulk/chessplan?new=1&block_id=161&types=1,2"

import urllib.request
import json
from bs4 import BeautifulSoup as BS
from datetime import date as today
import os

project_name = 'Дмитровский парк'

DATE_FILE_NAME = today.today().strftime('%d-%m-%Y') + '.json'
DATE = today.today().strftime('%d.%m.%Y')

def beautify_num(num):
    num = str(num)
    res = ''
    for i in range(1, len(num) + 1):
        res += num[-i]
        if i % 3 == 0:
            res += ' '
    return res[::-1]

def get_data_from_url(url):
    html = urllib.request.urlopen(url = url)
    html = BS(html, 'html.parser')
    html_json = json.loads(html.text)
    return html_json

# Запись полученных данных в файл
if not os.path.exists(project_name):
    os.mkdir(project_name)
with open(os.path.join(project_name, DATE_FILE_NAME), 'w') as f:
    json.dump(get_data_from_url(url), f)


# with open(f'{project_name}/{DATE_FILE_NAME}.json', "r") as f:
with open(os.path.join(project_name, DATE_FILE_NAME), 'w') as f:
    data = json.load(f)

# blocks = data['bulks']

for block in data['bulks']:
    if not os.path.exists(project_name):
        os.mkdir(project_name)
    sections = block['sections']
    for section in sections:
        if not os.path.exists(f'{project_name}/{block["name"]}'):
            os.mkdir(f'{project_name}/{block["name"]}')

        arr = []
        arr.append(DATE)
        for floor in list(section['floors'].keys())[::-1]:
            flats = section['floors'][floor]['flats']
            for flat in flats:
                if flat['status'] == 'free':
                    arr.append(beautify_num(flat['price']))
                elif flat['status'] == 'unavailable':
                    arr.append('')
                else:
                    arr.append('reserved')
        if not os.path.exists(f"{project_name}/{block['name']}/{section['name']}.csv"):
            with open(f"{project_name}/{block['name']}/{section['name']}.csv", 'a') as f:
                f.write('date/flat;')
                f.write(';'.join([str(x) for x in range(len(arr)-1)]))
                f.write(';\n')
        with open(f"{project_name}/{block['name']}/{section['name']}.csv", 'a') as f:
            f.write(';'.join(arr))
            f.write(';\n')