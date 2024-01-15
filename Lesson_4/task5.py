from multiprocessing import Process, current_process
from pathlib import Path


def file_listening(file: Path):
    words = 0
    if file.is_file():
        with file.open('r', encoding="utf-8") as file:
            for line in file:
                words += len(line.split())
        print(f"{current_process().name.upper()}: {words} words.")


if __name__ == '__main__':
    processes = []
    for file in Path.cwd().iterdir():
        proc = Process(target=file_listening,
                       args=(file,),
                       name=f"process_{file.name}",
                       daemon=True)
        processes.append(proc)
        proc.start()
    for p in processes:
        p.join()
