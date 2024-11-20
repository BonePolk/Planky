from dataclasses import dataclass

from Planky import PlankyProtocol, PlankyClient
from Planky.base.data.data import Data
from Planky.base.data.message import Message
from Planky.events.messageEvent import MessageEvent
from Planky.plankyServer import PlankyServer

server = PlankyServer("127.0.0.1", port=1111)

@dataclass
class PutTokenMessage(Message):
    token: str = ""

@dataclass
class GetTokenMessage(Message):
    pass

@dataclass
class TokenResult(Data):
    token: str = ""


class StorageProtocol(PlankyProtocol):
    async def parse_message(self, data: bytes):
        if data[0] == 0x00: return PutTokenMessage(token=data[1:].decode(errors="ignore"))
        if data[0] == 0x01: return GetTokenMessage()

        return await super().parse_message(data)

    async def pack_message(self, message: Data) -> bytes:
        if isinstance(message, TokenResult):
            return bytes([0x01]) + message.token.encode(errors="ignore")

        return b""

server.handler.set_protocol(StorageProtocol)

@server.on_message(PutTokenMessage)
async def put_token(client: PlankyClient, event: MessageEvent):
    event.message: PutTokenMessage

    client.storage.set("token", event.message.token)

@server.on_message(GetTokenMessage)
async def get_token(client: PlankyClient, event: MessageEvent):
    event.message: GetTokenMessage

    token = client.storage.get("token", default="NoToken")
    await client.send_data(TokenResult(token=token))

def mainloop():
    server.mainloop()

if __name__ == "__main__": mainloop()
