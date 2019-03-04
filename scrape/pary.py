
from bs4 import BeautifulSoup
import requests
import json
import os


def get_content(webpage):
    soup = BeautifulSoup(webpage, 'lxml')
    content = soup.find(id='content')
    return content

# url = 'http://www.csts.cz/cs/VysledkySoutezi/Souteze?rok=2018&mesic=01'
# r = requests.get(url, timeout=0.5)
# str(get_content(r.text))

results = json.load(open('data/vysledky.json', 'r'))
ids = [int(c['couple_id']) for r in results.values() for c in r['results']]

for par_id in ids:
    url = f'http://www.csts.cz/cs/VysledkySoutezi/Par/{par_id}'

    dir = os.path.join("data", "pary", "{:06d}".format(par_id // 1000 * 1000))
    fil = os.path.join(dir, "{:06d}.html".format(par_id))
    if os.path.isfile(fil):
        continue

    if par_id % 10 == 0:
        print(f'getting couple info from "{url}"..')

    for _ in range(10):
        try:
            r = requests.get(url, timeout=1.0)
        except (requests.ConnectTimeout, requests.ReadTimeout, requests.ConnectionError):
            print(f'server couldn\'t be reached.')
        else:
            break
    else:
        print('failed to fetch the webpage.')
        continue

    data = r.text
    content = get_content(data)

    # TODO: save to a file, if it doesn't exist yet.

    os.makedirs(dir, exist_ok=True)
    with open(fil, 'w') as f:
        f.write(str(content))
