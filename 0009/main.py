import csv
import json
import time
from datetime import datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup

path = str(Path(__file__).parent.resolve())

data_dir = f'{path}/data'
Path(data_dir).mkdir(parents=True, exist_ok=True)

start_time = time.time()


def get_data():
    cur_time = datetime.now().strftime('%Y-%m-%d_%H-%M')
    filename = f'labirint_{cur_time}'
    file_csv = f'{data_dir}/{filename}.csv'

    with open(file_csv, 'w') as f:
        writer = csv.writer(f)

        writer.writerow((
            'Название книги',
            'Автор',
            'Издательство',
            'Цена со скидкой',
            'Цена без скидки',
            'Процент скидки',
            'Наличие на складе'
        ))

    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    }
    url = 'https://www.labirint.ru/genres/2308/?available=1&paperbooks=1&display=table'

    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    pages_count = int(soup.find('div', class_='pagination-numbers').find_all('a')[-1].text)

    books_data = []
    for page in range(1, pages_count + 1):
        url = f'https://www.labirint.ru/genres/2308/?available=1&paperbooks=1&display=table&page={page}'

        response = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')

        books_items = soup.find('tbody', class_='products-table__body').find_all('tr')

        for bi in books_items:
            book_data = bi.find_all('td')

            try:
                book_title = book_data[0].find('a').text.strip()
            except Exception:
                book_title = 'Нет названия книги'

            try:
                book_author = book_data[1].text.strip()
            except Exception:
                book_author = 'Нет автора'

            try:
                book_publishing = book_data[2].find_all('a')
                book_publishing = ': '.join([bp.text for bp in book_publishing])
            except Exception:
                book_publishing = 'Нет издательства'

            try:
                book_new_price = int(book_data[3].find('span', class_='price-val').find('span').text.strip().replace(' ', ''))
            except Exception:
                book_new_price = 'Нет нового прайса'

            try:
                book_old_price = int(book_data[3].find('span', class_='price-gray').text.strip().replace(' ', ''))
            except Exception:
                book_old_price = 'Нет старого прайса'

            try:
                book_sale = round(((book_old_price - book_new_price) / book_old_price) * 100)
            except Exception:
                book_sale = 'Нет скидки'

            try:
                book_status = book_data[-1].text.strip()
            except Exception:
                book_status = 'Нет статуса'

            books_data.append({
                'book_title': book_title,
                'book_author': book_author,
                'book_publishing': book_publishing,
                'book_new_price': book_new_price,
                'book_old_price': book_old_price,
                'book_sale': book_sale,
                'book_status': book_status
            })

            with open(file_csv, 'a') as f:
                writer = csv.writer(f)

                writer.writerow((
                    book_title,
                    book_author,
                    book_publishing,
                    book_new_price,
                    book_old_price,
                    book_sale,
                    book_status
                ))

        print(f'Обработана страница {page}/{pages_count}')
        # time.sleep(1)

    with open(f'{data_dir}/{filename}.json', 'w') as f:
        json.dump(books_data, f, indent=4, ensure_ascii=False)


def main():
    get_data()
    finish_time = time.time() - start_time
    print(f'Затраченное время на работу скрипта: {finish_time}')


if __name__ == '__main__':
    main()
