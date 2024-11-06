from asyncio import StreamWriter


class Writer:
    def __init__(self, writer: StreamWriter, is_connected):
        self.writer = writer
        self.is_connected = is_connected

    def get_extra_info(self, key): return self.writer.get_extra_info(key)

    async def send_bytes(self, data: bytes): raise NotImplementedError