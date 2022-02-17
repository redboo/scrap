import ssl
from pathlib import Path

import requests
from lxml import html
from urllib3 import poolmanager

path = str(Path(__file__).parent.resolve())

downloads_dir = f'{path}/downloads'
Path(downloads_dir).mkdir(parents=True, exist_ok=True)


class TLSAdapter(requests.adapters.HTTPAdapter):

    def init_poolmanager(self, connections, maxsize, block=False):
        """Create and initialize the urllib3 PoolManager."""
        ctx = ssl.create_default_context()
        ctx.set_ciphers('DEFAULT@SECLEVEL=1')
        self.poolmanager = poolmanager.PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            ssl_version=ssl.PROTOCOL_TLS,
            ssl_context=ctx)


def get_data(url):
    session = requests.session()
    session.mount('https://', TLSAdapter())
    api = session.get(url)

    tree = html.document_fromstring(api.text)
    text_original = tree.xpath('//*[@id="click_area"]/div//*[@class="original"]/text()')
    text_translate = tree.xpath('//*[@id="click_area"]/div//*[@class="translate"]/text()')

    # TODO filename from url https://www.amalgama-lab.com/songs/n/nirvana/aero_zeppelin.html -> 'nirvana-aero_zeppelin.txt'

    with open(f'{downloads_dir}/text.txt', 'w', encoding='utf-8') as f:
        for original, translate in zip(text_original, text_translate):
            f.write(f'{original.strip()}\n{translate.strip()}\n')


def main():
    get_data('https://www.amalgama-lab.com/songs/n/nirvana/aero_zeppelin.html')


if __name__ == "__main__":
    main()
