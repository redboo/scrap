import json
from datetime import datetime
from os import sep
from pathlib import Path

import requests

path = str(Path(__file__).parent.resolve())

data_dir = path + sep + "data"
Path(data_dir).mkdir(parents=True, exist_ok=True)

headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "User-Agent": "Mozilla/5.0 (X11 Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36",
    "X-Is-Ajax-Request": "X-Is-Ajax-Request",
    "X-Requested-With": "XMLHttpRequest"
}

domain = 'https://roscarservis.ru'


def get_data():
    start_time = datetime.now()
    url = domain + '/catalog/legkovye/?form_id=catalog_filter_form&filter_mode=params&sort=asc&filter_type=tires&arCatalogFilter_458_1500340406=Y&set_filter=Y&isAjax=true&PAGEN_1={i}'
    r = requests.get(url=url.format(i=1), headers=headers)

    pages_count = r.json()['pageCount']

    data_list = []
    for page in range(1, pages_count + 1):
        r = requests.get(url=url.format(i=page), headers=headers)
        data = r.json()
        items = data['items']

        possible_stores = ["discountStores", "fortochkiStores", "commonStores"]
        for item in items:
            total_amount = 0

            stores = []
            for ps in possible_stores:
                if ps in item:
                    if item[ps] is None or len(item[ps]) < 1:
                        continue
                    else:
                        for store in item[ps]:
                            total_amount += int(store['AMOUNT'])

                            stores.append({
                                "store_name": store['STORE_NAME'],
                                "store_price": store['PRICE'],
                                "store_amount": int(store['AMOUNT'])
                            })

            data_list.append({
                'name': item['name'],
                'price': item['price'],
                'url': domain + item['url'],
                'img_url': domain + item['imgSrc'],
                'stores': stores,
                'total_amount': total_amount
            })

        print(f'[INFO] Обработано {page}/{pages_count} страниц')

    cur_time = datetime.now().strftime('%Y-%m-%d_%H-%M')

    with open(f'{data_dir}/data_{cur_time}.json', 'a') as f:
        json.dump(data_list, f, indent=4, ensure_ascii=False)

    diff_time = datetime.now() - start_time
    print(diff_time)


def main():
    get_data()


if __name__ == '__main__':
    main()
