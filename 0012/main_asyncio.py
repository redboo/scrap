import asyncio
from time import time

import aiohttp

start_time = time()
brands_page = 'https://ozon.ru/brand'
all_data = []


async def get_page_data(session, category: str, page_id: int) -> str:
    url = f'{brands_page}/{category}/?page={page_id}' if page_id else f'{brands_page}/{category}'
    async with session.get(url) as resp:
        assert resp.status == 200
        print(f'[INFO] get url: {url}')
        resp_text = await resp.text()
        all_data.append(resp_text)
        return resp_text


async def load_site_data():
    categories_list = [
        'playstation-79966341',
        'adidas-144082850',
        'bosch-7577796',
        'lego-19159896',
        'shell-140564506'
    ]
    async with aiohttp.ClientSession() as session:
        tasks = []
        for cat in categories_list:
            for page_id in range(1, 100):
                task = asyncio.create_task(get_page_data(session, cat, page_id))
                tasks.append(task)
                # process text and do whatever we need...
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(load_site_data())
    print('\n[Time taken]: ', time() - start_time)
