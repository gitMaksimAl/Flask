import threading

import requests
from threading import Thread


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
    file_name = f"./artefacts/thread_{threading.current_thread().name}"
    with open(file_name, 'w', encoding="utf-8") as file:
        file.write(resp.text)


if __name__ == '__main__':
    threads = []
    for url in urls:
        thread = Thread(target=download, args=(url,),
                        daemon=True,
                        name=url.replace("https://", "").replace('/', ''))
        threads.append(thread)
        thread.start()
    for t in threads:
        t.join()
