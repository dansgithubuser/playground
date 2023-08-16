import asyncio

async def f():
    await asyncio.sleep(1)
    print('f')

asyncio.run(f())  # blocks
print('done')
