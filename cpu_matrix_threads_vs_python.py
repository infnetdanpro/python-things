import threading
import httpx
import asyncio
import time

import numpy as np


if __name__ == '__main__':
    limit = 100

    # Classic Asyncio code
    async def test_async(*_, **__):
        for a in range(1000*2):
            np.matrix('1 2 3; 4 5 6; 7, 8, 9')

    coros = []
    for number in range(limit):
        coros.append(test_async(number))

    loop = asyncio.get_event_loop()
    start = time.time()
    results = loop.run_until_complete(asyncio.gather(*coros))
    time_result = time.time() - start
    print('Asyncio tasks ends', time_result, 'seconds')

    # Using threads
    # prepare list to fill results (checking real results)
    sync_results = [0] * limit

    def test_sync(*_, **__):
        for a in range(1000*2):
            np.matrix('1 2 3; 4 5 6; 7, 8, 9')

    threads = {}
    start = time.time()
    for number in range(limit):
        t = threading.Thread(target=test_sync, args=(number,))
        threads[number] = t
        t.start()

    for index, thread in threads.items():
        threads[index] = thread.join()
    time_result = time.time() - start
    print('Thread tasks ends', time_result, 'seconds')

#####################
# Results
# Asyncio tasks ends 11.948049068450928 seconds
# Thread tasks ends 12.23012661933899 seconds
