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
        ln_buf = await reader.receive_bytes(4)
        if len(ln_buf) < 4: raise TimeoutError
        length = struct.unpack(">I", ln_buf)[0]
        return RawMessage(await reader.receive_bytes(length))

    async def parse_message(self, data: bytes) -> Message:
        try:
            if self.check_ping(data): return PingMessage(data)
            return ParsedMessage(data)
        except Exception as e:
            raise ParseException(e)

    async def send(self, writer: Writer, message: PlankyData):
        payload = await self.pack_message(message)
        await writer.send_bytes(struct.pack(">I", len(payload)) + payload)

    async def pack_message(self, message: PlankyData) -> bytes:
        return message.payload

    async def send_bytes(self, writer: PlankyWriter, data: bytes):
        if self.is_connected():
            return await writer.send_bytes(struct.pack(">I", len(data)) + data)
        else:
            raise ConnectionError

