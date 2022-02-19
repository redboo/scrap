# -*- coding: utf-8 -*-
"""
Proxies download library
~~~~~~~~~~~~~~~~~~~~~

Parse and download proxies from
https://free-proxy-list.net/anonymous-proxy.html

"""


# import sys
from sys import argv
import logging
from os import makedirs, path as ospath

import requests
from bs4 import BeautifulSoup


class GetProxies():
    '''
    A class to download proxies.

    Attributes
    ----------
    filetype : str
        save file extension.

    Methods
    -------
    get_proxies(filetype=""):
        Download proxies data.
    data2json():
        Save data to JSON.
    data2txt():
        Save data to TXT.

    Getters
    ---
    filepath: str
        Return path of save file.
    list or datalist: list
        Return <list> collection of proxies.
    '''

    def __init__(
        self,
        ext: str = 'txt',
        path: str = None,
        file: str = None,
        filepath: str = None
    ):
        '''Parse and download proxies from
        https://free-proxy-list.net/anonymous-proxy.html

        Args:
            filetype (str, optional): save file extension. Defaults to 'txt'.
        '''
        self.path = path if path else ospath.dirname(argv[0])
        self.downloads_dir = f'{self.path}/downloads'
        self.file = file if file else 'proxies'
        self.ext = f'.{ext}' if ext else '.txt'
        self._filepath = filepath if filepath else f'{self.downloads_dir}/{self.file}{self.ext}'
        logging.debug(f'File extension is "{self.ext}"')
        makedirs(self.downloads_dir, exist_ok=True)
        self.data = []
        self.get_proxies()

    def get_proxies(self):
        logging.debug('get_proxies')
        url = "https://free-proxy-list.net/anonymous-proxy.html"

        req = requests.get(url)
        soup = BeautifulSoup(req.text, "lxml")

        rows = soup.find("div", class_="fpl-list").find("table").find("tbody").find_all("tr")
        for row in rows:
            td = row.find_all("td")

            if td[6].text.strip() == "no":
                ip = td[0].text.strip()
                port = td[1].text.strip()
                # protocol = "https" if td[6].text.strip() == "yes" else "http"
                protocol = "http"

                # proxies_list.append(
                #     {protocol: f"http://{ip}:{port}"}
                # )
                self.data.append(f'{ip}:{port}')

        match self.ext:
            case 'json':
                self.data2json()
            case _:
                self.data2txt()

    def data2json(self):
        import json
        logging.debug('data2json')
        with open(self._filepath, 'w') as f:
            f.write(json.dumps(self.data, indent=4, ensure_ascii=False))

    def data2txt(self):
        logging.debug('data2txt')
        with open(self._filepath, 'w') as f:
            f.write('\n'.join(self.data))

    filepath = property(lambda self: self._filepath)
    list = datalist = property(lambda self: self.data)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    GetProxies()
