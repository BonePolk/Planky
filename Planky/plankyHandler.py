import traceback
from asyncio import StreamWriter
from codecs import StreamReader

from Planky.base.handler import Handler
from Planky.events.connectEvent import ConnectEvent
from Planky.events.disconnectEvent import DisconnectEvent
from Planky.events.messageEvent import MessageEvent
from Planky.messages.pingMessage import PingMessage
from Planky.plankyProtocol import PlankyProtocol, ParseException
from Planky.plankyReader import PlankyReader
from Planky.plankyWriter import PlankyWriter


class PlankyHandler(Handler):
    """
    Handler for the Planky server.
    """
    def __init__(self, server):
        super().__init__(server)
        self.client_ip = None
        self.client_port = None

        self.protocol = PlankyProtocol(self.is_connected)

    async def handle_client(self, reader: StreamReader, writer: StreamWriter):
        self.client_ip, self.client_port = writer.get_extra_info("peername")

        await self._check_listeners(ConnectEvent(self.client_ip, self.client_port), "OnConnect")

        self.reader = PlankyReader(reader, self.is_connected)
        self.writer = PlankyWriter(writer, self.is_connected)

        self.client_connected = True
        try:
            while self.is_connected():
                message = await self.protocol.receive(self.reader)
                await self._check_listeners(MessageEvent(self.client_ip, self.client_port, message), "OnMessage")

                parsed_message = await self.protocol.parse_message(message.content)
                if isinstance(parsed_message, PingMessage): await self.protocol.send_ping(self.writer)
                await self._check_listeners(MessageEvent(self.client_ip, self.client_port, parsed_message), "OnMessage")
        except TimeoutError as e: pass
        except ParseException as e: print(traceback.format_exc())
        except Exception as e:
            print(traceback.format_exc())
            raise e
        finally:
            await self.close_connection()

    async def close_connection(self, description: str = None, code = 0):
        """
        Close connection.

        :param description: description of disconnect
        :param code: error code of disconnect
        """
        self.client_connected = False
        await self.writer.writer.drain()
        await self._check_listeners(DisconnectEvent(self.client_ip, self.client_port, description, code), "OnDisconnect")

