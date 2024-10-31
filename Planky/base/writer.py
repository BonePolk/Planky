from asyncio import StreamWriter


class Writer:
    def __init__(self, writer: StreamWriter, is_connected):
        self.writer = writer
        self.is_connected = is_connected

    async def send_bytes(self, data: bytes): raise NotImplementedError