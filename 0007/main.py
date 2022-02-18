import csv
import json
import time
from datetime import datetime
from os import sep
from pathlib import Path

import requests
from bs4 import BeautifulSoup

path = str(Path(__file__).parent.resolve())
domain = "https://shop.casio.ru"

data_dir = path + sep + "data"
Path(data_dir).mkdir(parents=True, exist_ok=True)


def get_all_pages():
    url = "https://shop.casio.ru/catalog/g-shock/"
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36"
    }

    r = requests.get(url=url, headers=headers)

    with open(f'{data_dir}/page_1.html', 'w') as f:
        f.write(r.text)

    with open(f'{data_dir}/page_1.html') as f:
        src = f.read()

    soup = BeautifulSoup(src, 'lxml')
    pages_count = int(soup.find('div', class_='bx-pagination-container').find_all('a')[-2].text)

    for i in range(1, pages_count + 1):
        url = f'{domain}/catalog/g-shock/?PAGEN_1={i}'

        r = requests.get(url=url, headers=headers)

        with open(f'{data_dir}/page_{i}.html', 'w') as f:
            f.write(r.text)
            print(f'[INFO] Страница #{i} загружена')

        time.sleep(2)

    return pages_count + 1


def collect_data(pages_count):
    cur_date = datetime.now().strftime('%Y-%m-%d')

    with open(f'{data_dir}/csv_{cur_date}.csv', 'w') as f:
        writer = csv.writer(f)

        writer.writerow(
            (
                "Артикул",
                "Ссылка",
                "Цена"
            )
        )

    data = []
    for page in range(1, pages_count):
        with open(f'{data_dir}/page_{page}.html') as f:
            src = f.read()

            soup = BeautifulSoup(src, 'lxml')
            items_cards = soup.find_all('a', class_='product-item__link')

        for item in items_cards:
            product_url = domain + item.get('href')
            product_article = item.find('p', class_='product-item__articul').text.strip()
            product_price = item.find('p', class_='product-item__price').text.lstrip('руб. ').strip()

            # print(f'Artikul: {product_article} - Price: {product_price} - URL: {product_url}')

            data.append({
                'product_article': product_article,
                'product_url': product_url,
                'product_price': product_price
            })

            with open(f'{data_dir}/csv_{cur_date}.csv', 'a') as f:
                writer = csv.writer(f)

                writer.writerow((
                    product_article,
                    product_url,
                    product_price
                ))

        print(f'[INFO] Обработана страница {page}/{pages_count-1}')

    with open(f'{data_dir}/data_{cur_date}.json', 'a') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def main():
    pages_count = get_all_pages()
    collect_data(pages_count=pages_count)


if __name__ == '__main__':
    main()
