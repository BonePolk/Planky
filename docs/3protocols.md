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

### Example

```python
import json
from dataclasses import dataclass
from typing import Type

from Planky import PlankyProtocol, PlankyData
from Planky.base.data.message import Message


@dataclass
class ErrorMessage(Message):
    description: str = ""
    code: int = 0
    

@dataclass
class RunCommandMessage(Message):
    command: str = ""

class JsonProtocol(PlankyProtocol):
    async def parse_message(self, data: bytes) -> Message:

        try:
            json_message = json.loads(data.decode(errors="ignore"))
        except json.JSONDecodeError as e:
            return ErrorMessage(description=str(e), code=-2)

        if "command" not in json_message: return ErrorMessage(code=-2, description="No found 'command' in payload")
        return RunCommandMessage(command=json_message["command"])

    async def pack_message(self, message: PlankyData) -> bytes:
        return json.dumps(message).encode()
```

And now you can connect protocol to your server handler

```python
from Planky.events.messageEvent import MessageEvent
from Planky.plankyData import PlankyData
from Planky.plankyServer import PlankyServer

from jsonProtocol import JsonProtocol, ErrorMessage, RunCommandMessage

server = PlankyServer("127.0.0.1", port=1111)
server.handler.set_protocol(JsonProtocol)


@server.on_message(ErrorMessage)
async def error_message(client, event: MessageEvent):
    event.message: ErrorMessage
    
    print(f"Error event: {event} client: {client}")

@server.on_message(RunCommandMessage)
async def run_message(client, event: MessageEvent):
    event.message: RunCommandMessage
    
    print(f"Run {event.message.command}")

def mainloop():
    server.mainloop()

    
if __name__ == "__main__": mainloop()
```

### Custom protocol methods

You can create your own protocol. 

To create custom protocol you need to implement `PlankyProtocol` class and override methods.

#### pack_message

`async def pack_message(self, message: Data) -> bytes:`

Method serializes data to bytes message content.

Instead of instance of Data you can use custom implementation of Data.

#### parse_message

`async def parse_message(self, data: bytes) -> Message:`

Method deserializes bytes message content to instance of Message or your implementation of Message.

#### check_ping

`def check_ping(self, data: bytes):`

Method checks if data is ping message.
It used by `PlankyProtocol` in Protocol.parse_message to check if data is ping message.

#### generate_ping

`def generate_ping(self):`

Method generates ping message. It used to send ping message to client.