from Planky.events.connectEvent import ConnectEvent
from Planky.events.disconnectEvent import DisconnectEvent
from Planky.events.messageEvent import MessageEvent
from Planky.messages.parsedMessage import ParsedMessage
from Planky.messages.pingMessage import PingMessage
from Planky.messages.rawMessage import RawMessage
from Planky.plankyServer import PlankyServer

server = PlankyServer("127.0.0.1", port=1112)
server.load_server_cert("public.pem", "private.pem")

@server.on_connect(filter=lambda event: event.client_ip == "127.0.0.1")
async def connect(handler, event: ConnectEvent):
    print(f"Client connected {event}")

@server.on_message(RawMessage)
async def message(handler, event: MessageEvent):
    print(f"Client sended message {event}")

@server.on_message(PingMessage)
async def ping(handler, event: MessageEvent):
    print(f"Client sended ping {event}")

@server.on_message(ParsedMessage)
async def parsed_message(handler, event: MessageEvent):
    print(f"Client sended parsed message {event}")

@server.on_disconnect()
async def disconnect(handler, event: DisconnectEvent):
    print(f"Client disconnected {event}")


def mainloop():
    server.mainloop()


if __name__ == "__main__": mainloop()

