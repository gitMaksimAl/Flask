from threading import Thread, current_thread
from pathlib import Path


def file_listening(file: Path):
    words = 0
    if file.is_file():
        with file.open('r', encoding="utf-8") as file:
            for line in file:
                words += len(line.split())
        print(f"{current_thread().name.upper()}: {words} words.")


if __name__ == '__main__':
    threads = []
    for file in Path.cwd().iterdir():
        thread = Thread(target=file_listening,
                        args=(file,),
                        name=f"thread_{file.name}",
                        daemon=True)
        threads.append(thread)
        thread.start()
    for t in threads:
        t.join()
