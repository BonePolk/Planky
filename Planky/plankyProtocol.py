import struct

from Planky.base.data.message import Message
from Planky.base.protocol import Protocol
from Planky.base.writer import Writer
from Planky.messages.parsedMessage import ParsedMessage
from Planky.messages.pingMessage import PingMessage
from Planky.messages.rawMessage import RawMessage
from Planky.plankyData import PlankyData
from Planky.plankyReader import PlankyReader
from Planky.plankyWriter import PlankyWriter


class ParseException(Exception):
    pass

class PlankyProtocol(Protocol):
    async def receive(self, reader: PlankyReader):
        """
        Receive message from client

        :param reader: Reader from handler
        :return: Message from client
        """
        ln_buf = await reader.receive_bytes(4)
        if len(ln_buf) < 4: raise TimeoutError
        length = struct.unpack(">I", ln_buf)[0]
        return RawMessage(await reader.receive_bytes(length))

    async def parse_message(self, data: bytes) -> Message:
        """
        Parse message from client

        :param data: Some message content from client
        :return: Parsed message instance
        """
        try:
            if self.check_ping(data): return PingMessage(data)
            return ParsedMessage(data)
        except Exception as e:
            raise ParseException(e)

    async def send(self, writer: Writer, message: PlankyData):
        """
        Serialize and send message to client.

        _Used by handler.send_data_

        :param writer: Writer from handler
        :param message: Your data to send to client
        :return:
        """
        payload = await self.pack_message(message)
        await writer.send_bytes(struct.pack(">I", len(payload)) + payload)

    async def pack_message(self, message: PlankyData) -> bytes:
        """
        Serialize Data to message content

        :param message: Your data to send to client
        :return: Message content to send to client
        """
        return message.payload

    async def send_bytes(self, writer: PlankyWriter, data: bytes):
        """
        Sending message content to client

        :param writer: Writer from handler
        :param data: Serialized message content

        :raises ConnectionError: if client is not connected or disconnected
        """
        if self.is_connected():
            return await writer.send_bytes(struct.pack(">I", len(data)) + data)
        else:
            raise ConnectionError

