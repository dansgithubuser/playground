#!/usr/bin/env python3

from dbus_next import Message, MessageType
from dbus_next.aio import MessageBus

import asyncio
import pprint

def message_print(msg):
    pprint.pprint({
        'destination': msg.destination,
        'path': msg.path,
        'member': msg.member,
        'signature': msg.signature,
        'body': msg.body,
    })

async def main():
    bus = await MessageBus().connect()
    reply = await bus.call(
        Message(
            destination='org.freedesktop.DBus',
            path='/org/freedesktop/DBus',
            member='AddMatch',
            signature='s',
            body=["member='test', interface='com.playground.dbus_next'"],
        ),
    )
    assert reply.message_type == MessageType.METHOD_RETURN
    bus.add_message_handler(message_print)
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
