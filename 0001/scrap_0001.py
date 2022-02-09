# pip install pytablewriter
from pathlib import Path
import requests
from bs4 import BeautifulSoup
import pytablewriter


url = 'https://rb.ru/news/100-best-startups/'
cur_dir = str(Path(__file__).parent.resolve())
data_path = cur_dir + '/data'
index_file = data_path + '/index.html'
md_file = data_path + '/data_table.md'
headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36"
}

Path(data_path).mkdir(parents=True, exist_ok=True)

if not Path(index_file).is_file():
    req = requests.get(url, headers=headers)
    src = req.text
    # print(src)

    with open(index_file, 'w') as f:
        f.write(src)
        print(f'{index_file} successfully created.')

with open(index_file) as f:
    src = f.read()

soup = BeautifulSoup(src, 'lxml')

# данные таблицы
trs = soup.find(class_="article__table__wrapper").find_all('tr')
# print(ths)

# with open(data_table_md, 'w') as f:
#     f.write()

writer = pytablewriter.MarkdownTableWriter()
writer.table_name = "100 лучших стартапов в сфере образовательных технологий"
writer.value_matrix = []
for idx, item in enumerate(trs):
    tds = item.find_all('td')

    if idx > 0:
        writer.value_matrix.append([i.text for i in tds])
    else:
        writer.header_list = [i.text for i in tds]


# writer.header_list = ["zone_id", "country_code", "zone_name"]
# writer.value_matrix = [
#     ["1", "AD", "Europe/Andorra"],
#     ["2", "AE", "Asia/Dubai"],
#     ["3", "AF", "Asia/Kabul"],
#     ["4", "AG", "America/Antigua"],
#     ["5", "AI", "America/Anguilla"],
# ]

# writer.write_table()
writer.dump(md_file)

print(f'Работа завершена. Файл "{md_file}" записан.')
