from asyncio import StreamReader, StreamWriter
from collections import defaultdict
from typing import Type

from Planky.base.data.data import Data
from Planky.base.listener import Listener
from Planky.base.protocol import Protocol
from Planky.base.server import Server


class Handler:
    def __init__(self, server: Server):
        self.reader = None
        self.writer = None

        self.server = server
        self.client_connected = False
        self.protocol = None
        self.listeners = defaultdict(list[Listener])

    def is_connected(self): return self.server.connected and self.client_connected
    def handle_client(self, reader: StreamReader, writer: StreamWriter): raise NotImplementedError
    def close_connection(self): raise NotImplementedError

    def set_protocol(self, protocol: Type[Protocol]):
        self.protocol = protocol(self.is_connected)

    def add_listener(self, listener): self.listeners[listener.__class__.__name__].append(listener)
    async def send_data(self, data: Data):
        await self.protocol.send(self.writer, data)

    async def _check_listeners(self, event, listener_name):
        for listener in self.listeners[listener_name]:
            await listener.check_event(event, self)
