import json
import logging
from os import makedirs, path
from sys import argv
from time import time

import requests

DIR = path.dirname(argv[0])

DOWNLOADS = f'{DIR}/downloads'
DATA = f'{DOWNLOADS}/data'
makedirs(DATA, exist_ok=True)

RESULT_FILE = f'{DOWNLOADS}/result_list.json'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
}
DOMAIN = 'https://landingfolio.com'


def get_data_file():
    # url = DOMAIN
    # r = requests.get(url, headers=headers)

    # with open(f'{DOWNLOADS}/index.html', 'w') as f:
    #     f.write(r.text)

    offset = 0
    img_count = 0
    result_list = []

    while True:
        url = f'https://s1.landingfolio.com/api/v1/inspiration/?offset={offset}'

        r = requests.get(url, headers=HEADERS)
        data = r.json()

        for item in data:
            if 'description' in item:

                images = item.get('images')
                img_count += len(images)

                for img in images:
                    img.update({'url': f'https://landingfoliocom.imgix.net/{img.get("url")}'})

                result_list.append(
                    {
                        'title': item.get('title'),
                        'description': item.get('description'),
                        'url': item.get('url'),
                        'images': images
                    }
                )
            else:
                with open(RESULT_FILE, 'a') as f:
                    json.dump(result_list, f, indent=4, ensure_ascii=False)

                return logging.info(f'✅ Work is finished. Images count is: {img_count}')

        logging.info(f'➕ Processed {offset}')
        offset += 1


def download_images(file_path):
    try:
        with open(file_path) as f:
            src = json.load(f)
    except Exception as e:
        return logging.exception(f'Could not load. {e}')

    items_len = len(src)
    count = 1
    for item in src[:100]:
        item_name = item.get('title')
        item_images = item.get('images')
        item_path = f'{DATA}/{item_name}'

        makedirs(item_path, exist_ok=True)

        for image in item_images:
            r = requests.get(image['url'], headers=HEADERS)
            image_path = f'{item_path}/{image["type"]}.{image["url"].split(".")[-1]}'

            with open(image_path, 'wb') as f:
                f.write(r.content)

        logging.info(f'💾 Download {count}/{items_len}')
        count += 1

    return logging.info('✅ Work is finished!')


def main():
    start_time = time()

    get_data_file()
    download_images(RESULT_FILE)

    logging.info(f'\n⏱ [Time taken]: {time() - start_time}')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
