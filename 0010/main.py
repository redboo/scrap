import time
import requests
from bs4 import BeautifulSoup

from pathlib import Path

path = str(Path(__file__).parent.resolve())


def test_request(url, retry=5):
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    }

    try:
        response = requests.get(url=url, headers=headers)
        print(f'✅ {url} {response.status_code}')
    except Exception as e:
        time.sleep(3)
        if retry:
            print(f'❌ retry={retry} => {url}')
            return test_request(url, retry=(retry - 1))
        else:
            raise
    else:
        return response


def main():
    with open(f'{path}/books_urls.txt') as f:
        books_urls = f.read().splitlines()

    for book_url in books_urls:
        try:
            r = test_request(url=book_url)
            soup = BeautifulSoup(r.text, 'lxml')
            print(f'{soup.title.text}\n{"-" * 20}')
        except Exception:
            print(f'{"-" * 20}')
            continue


if __name__ == "__main__":
    main()
