#!/usr/bin/env python3

from dbus_next import Message, MessageType
from dbus_next.aio import MessageBus

import asyncio
import pprint

async def main():
    bus = await MessageBus().connect()
    for i in range(5):
        await bus.send(
            Message.new_signal(
                '/com/playground/dbus_next',
                'com.playground.dbus_next',
                'test',
                's',
                ['hello'],
            ),
        )
        await asyncio.sleep(1)

asyncio.run(main())
