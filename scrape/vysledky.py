
from bs4 import BeautifulSoup
import requests
import json


def get_results(webpage, cat_id):
    soup = BeautifulSoup(webpage, 'lxml')
    content = soup.find('div', id='content')
    description = content.div.text

    results, adjudicators = content.find_all('table', recursive=False)

    records = []
    rows = results.find_all('tr')
    for row in rows:
        cells = row.find_all('td')
        if len(cells) == 8:
            rank, number, couple, club, points, points_after, new_class, note = cells
            record = dict(rank=rank.text, number=number.text, couple=couple.text, couple_id=couple.a['href'].split('/')[-1], club=club.text, points=points.text, points_after=points_after.text, new_class=new_class.text, note=note.text.strip())
            records.append(record)
        elif len(cells) == 7:
            rank, number, couple, club, points, points_after, note = cells
            record = dict(rank=rank.text, number=number.text, couple=couple.text, couple_id=couple.a['href'].split('/')[-1], club=club.text, points=points.text, points_after=points_after.text, note=note.text.strip())
            records.append(record)
        elif len(cells) == 5:
            rank, number, couple, club, note = cells
            record = dict(rank=rank.text, number=number.text, couple=couple.text, couple_id=couple.a['href'].split('/')[-1], club=club.text, note=note.text.strip())
            records.append(record)
        elif len(cells) <= 1:
            pass # finale/semifinale/1.kolo/etc. header
        else:
            raise ValueError(len(cells), str(cells))

    return dict(
        id=cat_id,
        results=records,
        adjudicators=[a.text for a in adjudicators.find_all('div')]
        )


comps = json.load(open('data/souteze.json', 'r'))

results = {}
for i, comp in enumerate(comps):
    print(f"{i}/{len(comps)} - {comp['date']} - {comp['name']}")

    for cat in comp['cats']:
        if cat['id'] in results.keys():
            continue
        # print(f"getting result for competition {cat['id']}..")

        url = f"http://www.csts.cz/cs/VysledkySoutezi/Soutez/{cat['id']}"

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
        res = get_results(data, cat['id'])

        results[cat['id']] = res



comps = {}

for y in range(2001, 2019):
    for m in range(1, 13):
        if (y, m) in comps.keys(): continue
        print(f'getting comps for {y}-{m}..')
        url = f'http://www.csts.cz/cs/VysledkySoutezi/Souteze?rok={y}&mesic={m:02}'


        data = r.text

        cs = get_comps(url)
        print(f'got {len(cs)} records.')
        comps[(y, m)] = cs


comps_cat = []
for comp in comps.values():
    comps_cat += comp

json.dump(comps_cat, open('data/souteze.json', 'w'), sort_keys=True, indent=4, separators=(',', ': '))
