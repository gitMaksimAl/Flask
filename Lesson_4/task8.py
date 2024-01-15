from threading import Thread, current_thread
from time import time
from pywebcopy import save_website
from pathlib import Path


START_TIME = time()


def website(url: str, folder: Path) -> None:
    file_name = f"{current_thread().name.upper()}_" \
                f"{url.replace('https://', '').replace('/', '')}"
    save_website(
        url=url,
        project_folder=folder.name,
        project_name=file_name,
        bypass_robots=True,
        debug=True,
        delay=None
    )
    print(f"Downloaded at time {time() - START_TIME}")


if __name__ == '__main__':
    urls = ["https://megaseller.shop/",]
    threads = []
    for url in urls:
        print("Create threads...")
        t = Thread(
            target=website,
            args=(url, Path.cwd().joinpath("artefacts")),
            name=f"thread_{url}",
            daemon=True
        )
        t.start()
    for t in threads:
        print("Join threads...")
        t.join()
