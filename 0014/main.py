import json
from os import path
from sys import argv

import requests
from bs4 import BeautifulSoup

DIR = path.dirname(argv[0])
URL = 'https://browser-info.ru'


def get_js(soup):
    return soup.find('div', id="javascript_check").find_all('span')[1].text


def get_cookie(soup):
    return soup.find('div', id="cookie_check").find_all('span')[1].text


def get_flash(soup):
    return soup.find('div', id="flash_version").find_all('span')[1].text


def main():
    with open(f'{DIR}/config.json') as f:
        config = json.load(f)

    print(config)
    res = requests.get(URL).text
    soup = BeautifulSoup(res, 'lxml')

    if config['js'] is True:
        print(f'{"js".upper():>6}: {get_js(soup)}')
    if config['cookie'] is True:
        print(f'{"cookie".upper():>6}: {get_cookie(soup)}')
    if config['flash'] is True:
        print(f'{"flash".upper():>6}: {get_flash(soup)}')


if __name__ == "__main__":
    main()
