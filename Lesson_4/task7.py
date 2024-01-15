from threading import Thread, current_thread
from random import randint
from timeit import default_timer
from multiprocessing import Process, current_process
from asyncio import ensure_future, run, gather, create_task
from typing import Callable

arr = [randint(0, 101) for _ in range(1, 1_000_001)]


def time_it(func):
    start_time = default_timer()

    def wrapper(numb):
        func(numb)
        print(default_timer() - start_time)
    return wrapper


def async_time_it(func: Callable) -> Callable:
    start_time = default_timer()

    async def wrapper(args):
        await func(args)
        print(default_timer() - start_time)

    return wrapper


@time_it
def get_sum(arr: list[int]) -> int:
    return sum(arr)


@async_time_it
async def async_get_sum(arr):
    return sum(arr)


async def coor():
    # task = ensure_future(async_get_sum(arr))
    task = create_task(async_get_sum(arr))
    await task

if __name__ == '__main__':
    p = Process(
        target=get_sum,
        args=(arr,),
        name="PROCESS_1",
        daemon=True
    )
    p.start()
    t = Thread(
        target=get_sum,
        args=(arr,),
        name="THREAD_1",
        daemon=True
    )
    t.start()
    t.join()
    p.join()
    run(coor())
