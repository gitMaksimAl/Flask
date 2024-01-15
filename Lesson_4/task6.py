from asyncio import ensure_future, gather, current_task, run
from pathlib import Path


async def file_listening(file: Path):
    words = 0
    if file.is_file():
        with file.open('r', encoding="utf-8") as file:
            for line in file:
                words += len(line.split())
    print(f"{current_task().get_name().upper()}: {words} words.")


async def main():
    tasks = []
    for file in Path.cwd().iterdir():
        task = ensure_future(file_listening(file))
        task.set_name(f"task_{file.name}")
        tasks.append(task)
    await gather(*tasks)


if __name__ == '__main__':
    run(main())
