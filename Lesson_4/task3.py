from asyncio import ensure_future, gather, current_task, run
from aiohttp import ClientSession

urls = [
    "https://www.google.ru/",
    "https://gb.ru/",
    "https://ya.ru/",
    "https://www.python.org/",
    "https://habr.com/ru/all/",
    "https://ru.wikipedia.org/",
    "https://ru.hexlet.io/",
    "https://megaseller.shop/",
    "https://linux.org",
    "https://metanit.com/"
]


async def download(url: str) -> None:
    async with ClientSession() as session:
        async with session.get(url) as resp:
            text = await resp.text()
            file_name = f"./artefacts/async_{current_task().get_name()}.html"
            with open(file_name, 'w', encoding="utf-8") as file:
                file.write(text)


async def main():
    tasks = []
    for url in urls:
        task = ensure_future(download(url))
        task.set_name(f"task_{url.replace('https://', '').replace('/', '')}")
        tasks.append(task)
    await gather(*tasks)


if __name__ == '__main__':
    run(main())
