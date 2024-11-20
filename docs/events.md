from Planky.events.pingEvent import PingEvent

# Event handling

## **server.on_connect**

You can handle client connections with `server.on_connect` decorator.

```python
from Planky import PlankyServer, PlankyClient
from Planky.events.connectEvent import ConnectEvent

server = PlankyServer("127.0.0.1", port=1111)


@server.on_connect()
async def on_connect(client: PlankyClient, event: ConnectEvent):
    print(f"Client connected")


server.mainloop()
```

## **server.on_disconnect**

You can handle client disconnections with `server.on_disconnect` decorator.

```python
from Planky import PlankyServer, PlankyClient
from Planky.events.disconnectEvent import DisconnectEvent

server = PlankyServer("127.0.0.1", port=1111)


@server.on_disconnect()
async def on_disconnect(client: PlankyClient, event: DisconnectEvent):
    print(f"Client disconnected")


server.mainloop()
```

## **server.on_message**

You can handle client messages with `server.on_message` decorator.

```python
from Planky import PlankyServer, PlankyClient
from Planky.events.messageEvent import MessageEvent
from Planky.messages.parsedMessage import ParsedMessage
from Planky.messages.rawMessage import RawMessage
from Planky.messages.pingMessage import PingMessage

server = PlankyServer("127.0.0.1", port=1111)

@server.on_message(ParsedMessage) 
async def on_message(client: PlankyClient, event: MessageEvent):
    print(f"Client sent message {event.message}")

@server.on_message(PingMessage)
async def on_ping(client: PlankyClient, event: MessageEvent):
    print(f"Client sent ping")
    
@server.on_message(RawMessage)
async def on_raw_message(client: PlankyClient, event: MessageEvent):
    print(f"Client sent unparsed message or ping {event.message}")

server.mainloop()
```

## **server.on_message**

You can handle client messages with `server.on_ping` decorator the same as `server.on_message(PingMessage)`.

```python
from Planky import PlankyServer, PlankyClient
from Planky.events.pingEvent import PingEvent

server = PlankyServer("127.0.0.1", port=1111)

@server.on_ping() 
async def on_ping(client: PlankyClient, event: PingEvent):
    print(f"Client sent message {event}")

server.mainloop()
```