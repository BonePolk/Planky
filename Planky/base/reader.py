from asyncio import StreamReader


class Reader:
    def __init__(self, reader: StreamReader, is_connected):
        self.reader = reader
        self.is_connected = is_connected

    async def receive_bytes(self, length: int, timeout=5): raise NotImplementedError