
from bs4 import BeautifulSoup
import requests
import json


def get_comps(webpage):
    soup = BeautifulSoup(webpage, 'lxml')
    divs = soup.find(id='content').find_all('div', recursive=False)
    comps = []
    for comp in divs[1:]:
        date, name, place, results = comp.find_all('div', recursive=False)
        ress = []
        for res in results.find_all('a'):
            comp_id, cat = res['href'].split('/')[-1], res.text
            ress.append(dict(id=comp_id, name=cat))
        comps.append(dict(date=date.text, name=name.text, place=place.text, cats=ress))
    return comps


comps = {}

for y in range(2001, 2019):
    for m in range(1, 13):
        if (y, m) in comps.keys(): continue
        print(f'getting comps for {y}-{m}..')
        url = f'http://www.csts.cz/cs/VysledkySoutezi/Souteze?rok={y}&mesic={m:02}'

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

        cs = get_comps(url)
        print(f'got {len(cs)} records.')
        comps[(y, m)] = cs


comps_cat = []
for comp in comps.values():
    comps_cat += comp

json.dump(comps_cat, open('data/souteze.json', 'w'), sort_keys=True, indent=4, separators=(',', ': '))
