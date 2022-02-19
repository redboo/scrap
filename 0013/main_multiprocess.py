import logging
import multiprocessing
from os import makedirs, path
from time import time

import requests

from proxydl import GetProxies

start_time = time()

url = 'http://icanhazip.com'
directory = path.dirname(__file__)
downloads_dir = f'{directory}/downloads'
# makedirs(downloads_dir, exist_ok=True)
file = f'{downloads_dir}/proxies.txt'


def get_proxy_list():
    try:
        with open(file) as f:
            proxy_list = ''.join(f.readlines()).strip().split('\n')
        logging.info('Прокси файл уже существует')
    except FileNotFoundError:
        proxy_list = GetProxies().list
        logging.info('Прокси файл загружен успешно')

    logging.debug(proxy_list)
    return proxy_list


def handler(proxy):
    proxies = {
        'http': f'http://{proxy}',
        'https': f'http://{proxy}'
    }

    try:
        response = requests.get(url, proxies=proxies, timeout=2).text.strip()
        logging.info(f'✅ {response}')
    except Exception:
        logging.info(f'❌ {proxy} invalid')


def main():
    proxy_list = get_proxy_list()

    # with multiprocessing.Pool(multiprocessing.cpu_count()) as process:
    with multiprocessing.Pool(20) as process:
        process.map(handler, proxy_list)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
    logging.info('\n[Time taken]: ', time() - start_time)
