from asyncio import StreamReader
from codecs import StreamWriter

from Planky.base.client import Client
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

    def parse_extra(self):
        client_ip, client_port = self.writer.get_extra_info("peername")

        self.storage.set("client_ip", client_ip)
        self.storage.set("client_port", client_port)