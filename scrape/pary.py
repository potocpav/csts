
from bs4 import BeautifulSoup
import requests
import json


def get_content(webpage):
    soup = BeautifulSoup(webpage, 'lxml')
    content = soup.find(id='content')
    return content

# url = 'http://www.csts.cz/cs/VysledkySoutezi/Souteze?rok=2018&mesic=01'
r = requests.get(url, timeout=0.5)
str(get_content(r.text))

results = json.load(open('data/vysledky.json', 'r'))
ids = [int(c['couple_id']) for r in results.values() for c in r['results']]

for par_id in ids:
    if (y, m) in comps.keys(): continue
    if par_id % 100 == 0:
        print(f'getting couple {par_id}..')
    url = f'http://www.csts.cz/cs/VysledkySoutezi/Par/{par_id}'

    for _ in range(10):
        try:
            r = requests.get(url, timeout=0.5)
        except (requests.ConnectTimeout, requests.ReadTimeout):
            print(f'server couldn\'t be reached.')
        else:
            break
    else:
        print('failed to fetch the webpage.')
        continue

    data = r.text
    content = get_content(data)

    # TODO: save to a file, if it doesn't exist yet.
