import json
import time
from os import sep as SEP
from pathlib import Path

import requests
from bs4 import BeautifulSoup as bs


path = str(Path(__file__).parent.resolve())

data_dir = path + SEP + 'data'
Path(data_dir).mkdir(parents=True, exist_ok=True)

persons_url_list_file = data_dir + SEP + 'persons_url_list.txt'
data_json_file = data_dir + SEP + 'data.json'

if not Path(persons_url_list_file).is_file():
    persons_url_list = []

    for i in range(0, 740, 20):
        url = f'https://www.bundestag.de/ajax/filterlist/en/members/863330-863330?limit=20&noFilterSet=true&offset={i}'

        q = requests.get(url)
        res = q.content

        soup = bs(res, 'lxml')
        persons = soup.find_all(class_="bt-open-in-overlay")

        for person in persons:
            person_page_url = person.get('href')
            persons_url_list.append(person_page_url)

        time.sleep(1)

    with open(persons_url_list_file, 'a') as f:
        for line in persons_url_list:
            f.write(f'{line}\n')

with open(persons_url_list_file) as f:
    lines = [line.strip() for line in f.readlines()]

    data_dict = []
    for count, line in enumerate(lines, start=1):
        q = requests.get(line)
        result = q.content

        soup = bs(result, 'lxml')
        person = soup.find(class_="bt-biografie-name").find('h3').text.strip().split(',')
        person_name = person[0]
        person_party = person[1].strip()

        social_networks_urls = []

        social_networks = soup.find_all(class_="bt-link-extern")
        if social_networks:
            for item in social_networks:
                social_networks_urls.append(item.get('href'))

        data = {
            'person_name': person_name,
            'person_party': person_party,
            'social_networks': social_networks_urls
        }

        data_dict.append(data)

        with open(data_json_file, 'w') as f:
            json.dump(data_dict, f, indent=4)

        print(f'#{count}: {line} is done!')

        time.sleep(1)
