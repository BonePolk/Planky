from asyncio import StreamReader, StreamWriter
from collections import defaultdict
from typing import Type

from Planky.base.data.data import Data
from Planky.base.listener import Listener
from Planky.base.protocol import Protocol
from Planky.base.server import Server


class Handler:
    def __init__(self, server: Server):
        self.server = server
        self.client_connected = False
        self.protocol = None
        self.listeners = defaultdict(list[Listener])

    def is_connected(self): return self.server.connected
    def handle_client(self, reader: StreamReader, writer: StreamWriter): raise NotImplementedError
    def close_connection(self, client_id: str, description: str = None, code = 0):
        """
        Close connection.

        :param client_id: id of client
        :param description: description of disconnect
        :param code: error code of disconnect
        """
        raise NotImplementedError

    def set_protocol(self, protocol: Type[Protocol]):
        """
        Set custom protocol for handler.

        :param protocol: type of your own protocol
        """
        self.protocol = protocol(self.is_connected)

    def add_listener(self, listener):
        """
        Add listener to handler.

        _You can use **decorators from server class**   : on_connect, on_disconnect, on_message, on_ping_

        :param listener: instance of listener class
        """
        self.listeners[listener.__class__.__name__].append(listener)

    async def _check_listeners(self, event, client, listener_name):
        for listener in self.listeners[listener_name]:
            await listener.check_event(event, client)
