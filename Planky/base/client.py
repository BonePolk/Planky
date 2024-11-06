from asyncio import StreamReader, StreamWriter

from Planky.base.data.data import Data
from Planky.base.data.extra import Extra
from Planky.base.data.message import Message
from Planky.base.protocol import Protocol
from Planky.base.reader import Reader
from Planky.base.server import Server
from Planky.base.writer import Writer


class Client:

    def __init__(self, writer: StreamWriter, reader: StreamReader,
                 protocol: Protocol, server: Server):
        self.reader: Reader = Reader(reader, server.connected)
        self.writer: Writer = Writer(writer, server.connected)
        self.protocol = protocol
        self.extra: Extra = self.parse_extra()
        self.server: Server = server

        self.client_id = ""
        self.client_connected = False

    def is_connected(self):
        """
        Check if client is connected.

        :return: True if client is connected
        """
        return self.server.connected and self.client_connected

    def parse_extra(self) -> Extra:
        """
        Parse extra data from client.

        _For example ip and port of client_
        :return: Extra data
        """
        raise NotImplementedError

    async def receive(self) -> Message:
        """
        Receive message from client.

        :return: received message
        """

        return await self.protocol.receive(self.reader)

    async def send_ping(self):
        """
        Send ping to client.
        """
        await self.protocol.send_ping(self.writer)

    async def send_data(self, data: Data):
        """
        Send Data to client

        :param data: Your data to send to client
        """
        await self.protocol.send(self.writer, data)

    async def disconnect(self, description: str = None, code = 0):
        """
        Disconnect client.

        :param description: description of disconnect
        :param code: error code of disconnect
        """
        await self.writer.writer.drain()