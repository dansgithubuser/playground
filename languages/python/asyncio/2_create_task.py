import asyncio

async def f():
    await asyncio.sleep(1)
    print('f')

async def main():
    asyncio.create_task(f())  # concurrent
    await asyncio.sleep(2)
    print('done')

asyncio.run(main())
