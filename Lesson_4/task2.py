import requests
from multiprocessing import Process, current_process

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


def download(url: str) -> None:
    resp = requests.get(url)
    file_name = f"./artefacts/process_{current_process().name}.html"
    with open(file_name, 'w', encoding="utf-8") as file:
        file.write(resp.text)


if __name__ == '__main__':
    processes = []
    for url in urls:
        proc = Process(target=download, args=(url,),
                       daemon=True,
                       name=url.replace("https://", "").replace('/', ''))
        proc.start()
        processes.append(proc)
    for p in processes:
        p.join()
