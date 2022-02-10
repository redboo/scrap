import json
from os import sep as SEP
from pathlib import Path

import lxml
import requests
from bs4 import BeautifulSoup

from proxy_auth import proxies

path = str(Path(__file__).parent.resolve())

data_dir = path + SEP + "data"
Path(data_dir).mkdir(parents=True, exist_ok=True)

domain = "https://www.skiddle.com"
url = domain + "/festivals/search/"
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36"
}

# collect all fests URLs
fests_urls_list = []
# for i in range(0, 24, 24):
for i in range(0, 264, 24):
    url = f"https://www.skiddle.com/festivals/search/?ajaxing=1&sort=0&fest_name=&from_date=10%20Feb%202022&to_date=&maxprice=500&o={i}&bannertitle=April"

    req = requests.get(url, headers=headers, proxies=proxies)
    json_data = json.loads(req.text)
    html_response = json_data["html"]

    with open(f"{data_dir}{SEP}index_{i}.html", "w") as f:
        f.write(html_response)

    with open(f"{data_dir}{SEP}index_{i}.html") as f:
        src = f.read()

    soup = BeautifulSoup(src, "lxml")
    cards = soup.find_all(class_="card-details-link")

    for item in cards:
        fest_url = domain + item["href"]
        fests_urls_list.append(fest_url)

# collect fest info
fest_list_result = []
for count, url in enumerate(fests_urls_list, start=1):
    print(f"#{count}")
    print(url)

    req = requests.get(url=url, headers=headers, proxies=proxies)

    try:
        soup = BeautifulSoup(req.text, "lxml")
        fest_info_block = soup.find("div", class_="top-info-cont")

        fest_name = fest_info_block.find("h1").text.strip()
        fest_date = fest_info_block.find("h3").text.strip()
        fest_location_url = domain + fest_info_block.find("a", class_="tc-white").get("href")

        req = requests.get(url=fest_location_url, headers=headers, proxies=proxies)
        soup = BeautifulSoup(req.text, "lxml")

        contact_details = soup.find("h2", string="Venue contact details and info").find_next()
        items = [item.text for item in contact_details.find_all("p")]

        contact_details_dict = {}
        for contact_detail in items:
            contact_detail_list = contact_detail.split(":", 1)
            contact_details_dict[contact_detail_list[0].strip()] = contact_detail_list[1].strip()

        fest_list_result.append({
            "Fest name": fest_name,
            "Fest_date": fest_date,
            "Contacts data": contact_details_dict
        })

    except Exception as e:
        print(e)
        print("Damn... There was an error...")

with open(data_dir + SEP + "fest_list.json", "w") as f:
    json.dump(fest_list_result, f, indent=4, ensure_ascii=False)
