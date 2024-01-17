import asyncio
import multiprocessing
import threading
from abc import ABC, abstractmethod
import aiohttp
import re
from time import time
import requests
from typing import Callable


class FileDownloader(ABC):

    @abstractmethod
    def create_tasks(self, files_uri: list[str]):
        raise NotImplemented

    def is_file(self, file_uri: str) -> bool:
        file_pattern = r"[/[\w|\d]*\.[a-z]+\d?"
        return bool(re.match(file_pattern, file_uri.rsplit('/').pop()))

    @abstractmethod
    def get_files_from(self, uri: str) -> list[str]:
        raise NotImplemented

    @property
    @abstractmethod
    def tasks(self):
        raise NotImplemented

    @abstractmethod
    def download(self, uri: str, file: str):
        raise NotImplemented

    @abstractmethod
    def run(self, tasks: list | tuple):
        raise NotImplemented

    @abstractmethod
    def exit(self) -> None:
        raise NotImplemented


class AsyncFileDownloader(FileDownloader):
    import asyncio

    def __init__(self):
        self._tasks: dict[str, list] = {
            "urls": [],
            "files": [],
            "coroutines": []
        }
        self._start_time: float = 0.0

    def create_tasks(self, files_uri: list[str]):
        for uri in files_uri:
            delimiter = uri.rfind('/')
            url, file = uri[:delimiter], uri[delimiter + 1:]
            self._tasks["urls"].append(url)
            self._tasks["files"].append(file)
            self._tasks["coroutines"].append(self.download(url, file))

    async def download(self, uri: str, file: str):
        asyncio.current_task().set_name(file)
        start_time = time()
        async with aiohttp.ClientSession() as s:
            async with s.get(uri) as resp:
                data = await resp.content.read()
                with open(file, "wb+") as f:
                    f.write(data)
            print(f"{asyncio.current_task().get_name()}: download time - "
                  f"{time() - start_time:.2f} sec.")

    @property
    async def tasks(self) -> tuple:
        return await asyncio.gather(*self._tasks["coroutines"])

    def get_files_from(self, uri: str) -> list[str]:
        raise NotImplemented

    def run(self, tasks: asyncio.Future):
        self._start_time = time()
        asyncio.run(tasks)

    def exit(self):
        try:
            asyncio.get_event_loop().stop()
        except RuntimeError:
            pass
        finally:
            print(f"Total execution time: {time() - self._start_time:.2f} sec.")
            del self._tasks


# TODO: work about run and exit points, task cancellation not implemented
class ThreadsFileDownloader(FileDownloader):

    def __init__(self):
        self._tasks: dict[str, list] = {
            "urls": [],
            "files": [],
            "threads": []
        }
        self._start_time: float = 0.0

    def create_tasks(self, files_uri: list[str]):
        for uri in files_uri:
            delimiter = uri.rfind('/')
            url, file = uri[:delimiter], uri[delimiter + 1:]
            self._tasks["urls"].append(url)
            self._tasks["files"].append(file)
            self._tasks["threads"].append(
                threading.Thread(
                    target=self.download,
                    args=(uri, file),
                    name=file,
                    daemon=True
                )
            )

    def get_files_from(self, uri: str) -> list[str]:
        raise NotImplemented

    @property
    def tasks(self):
        return self._tasks["threads"]

    def download(self, uri: str, file: str):
        start_time = time()
        with requests.Session() as s:
            with s.get(uri) as resp:
                with open(file, "wb+") as f:
                    f.write(resp.content)
            print(f"{threading.current_thread().name}: download time - "
                  f"{time() - start_time:.2f} sec.")

    def cancel(self) -> None:
        raise NotImplemented

    def run(self, threads: list[threading.Thread]):
        self._start_time = time()
        for t in threads:
            t.run()

    def exit(self) -> None:
        try:
            for p in self._tasks["threads"]:
                p.join()
        except RuntimeError:
            pass
        finally:
            print(f"Total execution time: {time() - self._start_time:.2f} sec.")
            del self._tasks


# TODO: work about run and exit points, task cancellation not implemented
class ProcessFileDownloader(FileDownloader):

    def __init__(self):
        self._tasks: dict[str, list] = {
            "urls": [],
            "files": [],
            "processes": []
        }
        self._start_time: float = 0.0

    def create_tasks(self, files_uri: list[str]):
        for uri in files_uri:
            delimiter = uri.rfind('/')
            url, file = uri[:delimiter], uri[delimiter + 1:]
            self._tasks["urls"].append(url)
            self._tasks["files"].append(file)
            self._tasks["processes"].append(
                multiprocessing.Process(
                    target=self.download,
                    args=(uri, file),
                    name=file,
                    daemon=True
                )
            )

    def get_files_from(self, uri: str) -> list[str]:
        raise NotImplemented

    @property
    def tasks(self):
        return self._tasks["processes"]

    def download(self, uri: str, file: str):
        start_time = time()
        with requests.Session() as s:
            with s.get(uri) as resp:
                with open(file, "wb+") as f:
                    f.write(resp.content)
            print(f"{multiprocessing.current_process().name}: download time - "
                  f"{time() - start_time:.2f} sec.")

    def run(self, tasks: list[multiprocessing.Process]):
        self._start_time = time()
        for p in tasks:
            p.start()

    def exit(self) -> None:
        try:
            for p in self._tasks["processes"]:
                p.join()
        except RuntimeError:
            pass
        finally:
            print(f"Total execution time: {time() - self._start_time:.2f} sec.")
            del self._tasks
