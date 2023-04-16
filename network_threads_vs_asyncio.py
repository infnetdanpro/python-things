import threading

import httpx

if __name__ == '__main__':
    import asyncio
    import time

    limit = 100

    # Classic Asyncio code
    async def test_async(n):
        async with httpx.AsyncClient(timeout=100000) as client:
            resp = await client.get('https://qa02.dev.kopa.com/api/v1/debug/status_code/?code=200')
            return resp.status_code

    coros = []
    for number in range(limit):
        coros.append(test_async(number))

    loop = asyncio.get_event_loop()
    start = time.time()
    results = loop.run_until_complete(asyncio.gather(*coros))
    time_result = time.time() - start
    print('Asyncio tasks ends', time_result, 'ms')

    # Using threads
    # prepare list to fill results (checking real results)
    sync_results = [0] * limit

    def test_sync(n: int):
        with httpx.Client(timeout=100000) as client:
            resp = client.get('https://qa02.dev.kopa.com/api/v1/debug/status_code/?code=200')
            # print(resp.status_code)
            sync_results[n] = resp.status_code
            return resp.status_code

    threads = {}
    start = time.time()
    for number in range(limit):
        t = threading.Thread(target=test_sync, args=(number,))
        threads[number] = t
        t.start()

    for index, thread in threads.items():
        threads[index] = thread.join()
    time_result = time.time() - start
    print('Thread tasks ends', time_result, 'ms')
