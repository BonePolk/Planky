from Planky.events.connectEvent import ConnectEvent
from Planky.events.disconnectEvent import DisconnectEvent
from Planky.events.messageEvent import MessageEvent
from Planky.messages.parsedMessage import ParsedMessage
from Planky.messages.pingMessage import PingMessage
from Planky.messages.rawMessage import RawMessage
from Planky.plankyServer import PlankyServer

server = PlankyServer("127.0.0.1", port=1111)

@server.on_connect()
async def connect(client, event: ConnectEvent, ):
    print(f"Client connected {event} {client}")

@server.on_message(RawMessage)
async def message(client, event: MessageEvent):
    print(f"Client sended message {event}")

@server.on_message(PingMessage)
async def ping(client, event: MessageEvent):
    print(f"Client sended ping {event}")

@server.on_message(ParsedMessage)
async def parsed_message(client, event: MessageEvent):
    print(f"Client sended parsed message {event}")

@server.on_disconnect()
async def disconnect(client, event: DisconnectEvent):
    print(f"Client disconnected {event}")


def mainloop():
    server.mainloop()


if __name__ == "__main__": mainloop()

