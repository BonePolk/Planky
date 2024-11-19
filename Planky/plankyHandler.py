import secrets
import traceback
from asyncio import StreamWriter
from asyncio import StreamReader

from Planky.base.client import Client
from Planky.base.handler import Handler
from Planky.events.connectEvent import ConnectEvent
from Planky.events.disconnectEvent import DisconnectEvent
from Planky.events.messageEvent import MessageEvent
from Planky.messages.pingMessage import PingMessage
from Planky.plankyClient import PlankyClient
from Planky.plankyProtocol import PlankyProtocol, ParseException
from Planky.plankyReader import PlankyReader
from Planky.plankyWriter import PlankyWriter


class PlankyHandler(Handler):
    """
    Handler for the Planky server.
    """
    def __init__(self, server):
        super().__init__(server)

        self.protocol = PlankyProtocol(self.is_connected)
        self.clients = {}

    @staticmethod
    def generate_client_id() -> str:
        """
        Generate client id for new client

        :return: Generated client id
        """
        return secrets.token_hex(16)

    async def handle_client(self, reader: StreamReader, writer: StreamWriter):
        client = await self._create_client(reader, writer)

        await self._check_listeners(ConnectEvent(client.extra), client, "OnConnect")

        client.client_connected = True
        try:
            while client.is_connected():
                message = await client.receive()
                await self._check_listeners(MessageEvent(client.extra, message), client, "OnMessage")

                parsed_message = await self.protocol.parse_message(message.content)
                if isinstance(parsed_message, PingMessage): await client.send_ping()
                await self._check_listeners(MessageEvent(client.extra, parsed_message), client, "OnMessage")
        except (TimeoutError, ConnectionResetError) as e: pass
        except (ParseException, Exception) as e:
            print(traceback.format_exc())
            raise e
        finally:
            await self.close_connection(client.client_id)

    async def _create_client(self, reader: StreamReader, writer: StreamWriter) -> Client:
        client_id = self.generate_client_id()

        client = PlankyClient(writer, reader, self.protocol, self.server)
        client.client_id = client_id

        self.clients[client_id] = client

        return client

    async def close_connection(self, client_id: str, description: str = None, code = 0):
        client = self.clients[client_id]
        await client.disconnect()

        self.clients.pop(client_id)

        await self._check_listeners(DisconnectEvent(client.extra, description, code), client, "OnDisconnect")

