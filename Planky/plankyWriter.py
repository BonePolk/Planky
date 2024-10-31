from Planky.base.writer import Writer


class PlankyWriter(Writer):


    async def send_bytes(self, data: bytes):

        if self.is_connected():
            return self.writer.write(data)
        else:
            raise ConnectionError
