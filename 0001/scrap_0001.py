from pathlib import Path
from os import sep as SEP
import requests
from bs4 import BeautifulSoup
import pytablewriter


url = 'https://rb.ru/news/100-best-startups/'

path = str(Path(__file__).parent.resolve())

data_dir = path + SEP + 'data'
Path(data_dir).mkdir(parents=True, exist_ok=True)

index_file = data_dir + SEP + 'index.html'
md_file = data_dir + SEP + 'data_table.md'

headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36"
}


if not Path(index_file).is_file():
    req = requests.get(url, headers=headers)

    with open(index_file, 'w') as f:
        f.write(req.text)
        print(f'{index_file} successfully created.')

with open(index_file) as f:
    src = f.read()

soup = BeautifulSoup(src, 'lxml')

# данные таблицы
trs = soup.find(class_="article__table__wrapper").find_all('tr')

writer = pytablewriter.MarkdownTableWriter()
writer.table_name = "100 лучших стартапов в сфере образовательных технологий"
writer.value_matrix = []
for idx, item in enumerate(trs):
    tds = item.find_all('td')

    if idx > 0:
        writer.value_matrix.append([i.text for i in tds])
    else:
        writer.header_list = [i.text for i in tds]

# writer.write_table()
writer.dump(md_file)

print(f'Работа завершена. Файл "{md_file}" записан.')
