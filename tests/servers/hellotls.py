import struct
from dataclasses import dataclass
from enum import Enum

from Planky import PlankyServer
from Planky.base.data.data import Data
from Planky.base.data.message import Message
from Planky.events.messageEvent import MessageEvent
from Planky.messages.parsedMessage import ParsedMessage
from Planky.messages.pingMessage import PingMessage
from Planky.messages.rawMessage import RawMessage
from Planky.plankyProtocol import PlankyProtocol


@dataclass
class HelloMessage(Message):
    pass

@dataclass
class TimeMessage(Message):
    time: int = 0

class HelloCodes(Enum):
    Plain = 0
    Hello = 1
    Time = 2

@dataclass
class HelloData(Data):
    code: HelloCodes = HelloCodes.Plain
    time: int = 0
    payload: bytes = 0

class HelloProtocol(PlankyProtocol):
    async def parse_message(self, data: bytes) -> Message:
        if self.check_ping(data): return PingMessage(data)

        if data[0] == 0x00: return ParsedMessage(content=data[1:])
        if data[0] == 0x01: return HelloMessage(content=data[1:])
        if data[0] == 0x02: return TimeMessage(time=struct.unpack(">I", data[1:])[0])
        return RawMessage(data)

    async def pack_message(self, message: HelloData) -> bytes:
        msg = struct.pack(">B", message.code.value)

        if message.code == HelloCodes.Time: msg += str(message.time).encode()
        else:  msg += message.payload

        return msg

server = PlankyServer("127.0.0.1", port=1112)
server.load_server_cert("public.pem", "private.pem")

@server.on_message(HelloMessage)
async def hello(handler, event: MessageEvent):
    print(f"Hello {event.message}")
    await handler.send_data(HelloData(code=HelloCodes.Hello, payload=b"World!"))

@server.on_message(TimeMessage)
async def time(handler, event: MessageEvent):
    event.message: TimeMessage

    print(f"Time {event.message}")
    await handler.send_data(HelloData(code=HelloCodes.Time, time=event.message.time))

@server.on_message(ParsedMessage)
async def parsed(handler, event: MessageEvent):
    print(f"Parsed {event.message}")
    await handler.send_data(HelloData(code=HelloCodes.Plain, payload=event.message.content))

def mainloop():
    server.mainloop()


if __name__ == "__main__": mainloop()