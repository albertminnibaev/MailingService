import asyncio


def run_async(coroutine):
    loop = asyncio.get_event_loop()
    if loop.is_running():
        future = asyncio.run_coroutine_threadsafe(coroutine, loop)
        return future.result()
    else:
        return loop.run_until_complete(coroutine)
