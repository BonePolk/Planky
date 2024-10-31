from asyncio import sleep
from time import time

from Planky.base.reader import Reader


class PlankyReader(Reader):
    async def receive_bytes(self, length: int, timeout=5):
        if length == 0:
            return b""

        r = await self.reader.read(length)
        start_time = time()
        while len(r) < length and self.is_connected and time() - start_time < timeout:
            r += await self.reader.read(length - len(r))
            await sleep(0.01)

        if time() - start_time >= timeout:
            raise TimeoutError(f"Timeout reading {length} bytes for {timeout} seconds. Read {len(r)} bytes")

        return r