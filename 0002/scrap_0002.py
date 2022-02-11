import json
import random
import time
from os import sep as SEP
from pathlib import Path

import requests
from bs4 import BeautifulSoup

path = str(Path(__file__).parent.resolve())

data_dir = path + SEP + "data" + SEP
Path(data_dir).mkdir(parents=True, exist_ok=True)

projects_dir = data_dir + "projects" + SEP
Path(projects_dir).mkdir(parents=True, exist_ok=True)

index_file = data_dir + "index.html"
project_data_file = data_dir + "projects_data.json"


def get_data(url, cur_page: int = 1, projects_data_list: list = []):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36"
    }

    req = requests.get(url + f"&data[controls][pageNum]={cur_page}", headers=headers)
    json_response = json.loads(req.text)
    next_page = json_response["nextPage"]
    page_count = json_response["pageCount"]

    if cur_page == 1:
        print(f"Всего итераций: #{page_count}")

    with open(index_file, 'w') as f:
        f.write(json_response["items"])

    with open(index_file) as f:
        src = f.read()

    soup = BeautifulSoup(src, 'lxml')
    projects = soup.find('body').find_all("a", class_="projects_list_b", recursive=False)

    project_urls = [project.get("href") for project in projects]

    for project_url in project_urls:
        time.sleep(random.randrange(2, 4))
        project_req = requests.get(project_url, headers=headers)
        project_uid_html = project_url.split("/")[-1]
        project_file = projects_dir + project_uid_html

        with open(project_file, "w") as f:
            f.write(project_req.text)

        with open(project_file) as f:
            project_src = f.read()

        soup = BeautifulSoup(project_src, "lxml")
        project_data = soup.find(id='detail-content')

        try:
            project_logo = project_data.find(id="big_photo_view").find("img").get("src")
        except Exception:
            project_logo = "No project logo"

        try:
            project_name = project_data.find("h1").text
        except Exception:
            project_name = "No project name"

        try:
            project_description_raw = project_data.find('div', class_="main_d").text.strip().replace("\n\n", '\n').replace('\xa0', ' ').splitlines()
            project_short_description = [line.strip() for line in project_description_raw]
            project_short_description = '\n'.join(project_short_description)
        except Exception:
            project_short_description = "No project short description"

        try:
            project_full_description = project_data.find(id="IDEA").find("div", class_="i_d").text.strip()
        except Exception:
            project_full_description = "No project full description"

        projects_data_list.append(
            {
                "Имя проекта": project_name,
                "URL логотипа проекта": project_logo,
                "Короткое описание проекта": project_short_description,
                "Полное описание проекта": project_full_description
            }
        )

    if not next_page == "last":
        print(f"Итерация #{cur_page} завершена, осталось итераций #{page_count - cur_page}")
        time.sleep(random.randrange(2, 4))
        get_data(url, next_page, projects_data_list)
    else:
        with open(project_data_file, "a") as f:
            json.dump(projects_data_list, f, indent=4, ensure_ascii=False)
        print("Сбор данных завершен")
        return


def main():

    # get_data("https://ru.startup.network/startups/")
    get_data(
        "https://ru.startup.network/local/ajax/projects.php?\
    data[action]=getNextPageProjects\
    &data[controls][pagePrevNum]=first\
    &data[controls][goal]=invest\
    &data[controls][curDir]=%2Fstartups%2F\
    &data[controls][goalSubType]=startups")


if __name__ == "__main__":
    main()
