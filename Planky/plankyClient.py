from asyncio import StreamReader
from codecs import StreamWriter

from Planky.base.client import Client
from Planky.base.data.extra import Extra
from Planky.plankyReader import PlankyReader
from Planky.plankyWriter import PlankyWriter


class PlankyClient(Client):
    """
    A default implementation of Planky client.
    """
    def __init__(self, writer: StreamWriter, reader: StreamReader,
                 protocol, server):
        super().__init__(writer, reader, protocol, server)
        self.writer = PlankyWriter(writer, self.is_connected)
        self.reader = PlankyReader(reader, self.is_connected)

    def parse_extra(self) -> Extra:
        client_ip, client_port = self.writer.get_extra_info("peername")
        return Extra(client_ip=client_ip, client_port=client_port)

