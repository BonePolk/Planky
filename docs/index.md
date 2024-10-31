# Quick Start

```python
from Planky.events.messageEvent import MessageEvent
from Planky.messages.parsedMessage import ParsedMessage
from Planky.plankyData import PlankyData
from Planky.plankyServer import PlankyServer

server = PlankyServer("127.0.0.1", port=1111)

@server.on_message(ParsedMessage)
async def parsed_message(handler, event: MessageEvent):
    if event.message.content == b"hello": 
        await handler.send_data(PlankyData(payload=b"world"))
    else:
        await handler.send_data(PlankyData(payload=event.message.content))

if __name__ == "__main__":
    server.mainloop()
```