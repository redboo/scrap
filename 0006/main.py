from os import sep as SEP
from pathlib import Path
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

path = str(Path(__file__).parent.resolve())

data_dir = path + SEP + "data" + SEP
Path(data_dir).mkdir(parents=True, exist_ok=True)

domain = "https://tury.ru"


def get_data(url):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36"
    }

    # r = requests.get(url=url, headers=headers)

    # with open(data_dir + "index.html", "w") as f:
    #     f.write(r.text)

    # get hotels urls
    r = requests.get("https://api.rsrv.me/hc.php?a=hc&most_id=1317&sort=most", headers=headers)
    soup = BeautifulSoup(r.text, "lxml")

    hotels_cards = soup.find_all("div", class_="hotel_card_dv")

    for hotel_card in hotels_cards:
        hotel_url = hotel_card.find("a").get("href")
        print(hotel_url)


def get_data_with_selenium(url):
    options = webdriver.FirefoxOptions()
    options.set_preference("general.useragent.override", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36")

    try:
        driver = webdriver.Firefox(
            executable_path="/home/redboo/Code/scrap/0006/geckodriver",
            options=options
        )
        driver.get(url=url)
        time.sleep(5)

        with open(data_dir + "index_selenium.html", "w") as f:
            f.write(driver.page_source)

    except Exception as e:
        print(e)
    finally:
        driver.close()
        driver.quit()

    with open(data_dir + "index_selenium.html") as f:
        src = f.read()
        soup = BeautifulSoup(src, "lxml")

        hotels_cards = soup.find_all("div", class_="hotel_card_dv")

        for hotel_card in hotels_cards:
            hotel_url = domain + hotel_card.find("a").get("href")
            print(hotel_url)


def main():
    # get_data("https://tury.ru/hotel/most_luxe.php")
    get_data_with_selenium("https://tury.ru/hotel/most_luxe.php")


if __name__ == '__main__':
    main()
