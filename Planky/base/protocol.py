from Planky.base.data.data import Data
from Planky.base.reader import Reader
from Planky.base.writer import Writer


class Protocol:
    def __init__(self, is_connected):
        self.is_connected = is_connected

    async def send_ping(self, writer: Writer):
        await self.send_bytes(writer, self.generate_ping())

    def check_ping(self, data: bytes):
        return not data

    def generate_ping(self):
        return b''

    async def receive(self, reader: Reader): raise NotImplementedError
    async def parse_message(self, data: bytes): raise NotImplementedError
    async def send(self, writer: Writer, message: Data): raise NotImplementedError
    async def pack_message(self, message: Data): raise NotImplementedError
    async def send_bytes(self, writer: Writer, data: bytes): raise NotImplementedError
