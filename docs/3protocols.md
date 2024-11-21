# Default and custom protocols

## Default protocol `PlankyProtocol`

You can use default protocol `PlankyProtocol` from `Planky` module. 

It parses message as `PingMessage` if message is empty else `ParsedMessage`.

**ParsedMessage** contains message content.

For example simple echo server:
```python
from Planky.events.messageEvent import MessageEvent
from Planky.messages.parsedMessage import ParsedMessage
from Planky.plankyData import PlankyData
from Planky.plankyServer import PlankyServer

server = PlankyServer("127.0.0.1", port=1111)

@server.on_message(ParsedMessage)
async def parsed_message(client, event: MessageEvent):
    print(f"Received {event}")
    await client.send_data(PlankyData(event.message.content))


def mainloop():
    server.mainloop()


if __name__ == "__main__": mainloop()
```

## Custom protocols

You can create your own protocol. 

To create custom protocol you need to inherit `PlankyProtocol` class and override methods.

- **pack_message**

`async def pack_message(self, message: Data) -> bytes:`

Method serializes data to bytes message content.
Instead of instance of Data you can use custom implementation of Data.

- **parse_message**

`async def parse_message(self, data: bytes) -> Message:`

Method deserializes bytes message content to instance of Message or your implementation of Message.

- **check_ping**

`def check_ping(self, data: bytes):`

Method checks if data is ping message.
It used by `PlankyProtocol` in Protocol.parse_message to check if data is ping message.

- **generate_ping**

`def generate_ping(self):`

Method generates ping message. It used to send ping message to client.