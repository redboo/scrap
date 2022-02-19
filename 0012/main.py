from time import time

import requests

start_time = time()
brands_page = 'https://ozon.ru/brand'
headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
}


def get_page_data(category: str, page_id: int) -> str:
    url = f'{brands_page}/{category}/?page={page_id}' if page_id else f'{brands_page}/{category}'
    print(f'[INFO] get url: {url}')
    return requests.get(url).text


def load_site_data():
    categories_list = [
        'playstation-79966341',
        'adidas-144082850',
        'bosch-7577796',
        'lego-19159896',
        'shell-140564506'
    ]
    for cat in categories_list:
        for page_id in range(1, 100):
            text = get_page_data(cat, page_id)
            # print(text)
            # process text and do whatever we need...


if __name__ == "__main__":
    load_site_data()
    print('\n[Time taken]: ', time() - start_time)
