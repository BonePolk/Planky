from Planky.events.messageEvent import MessageEvent
from Planky.messages.parsedMessage import ParsedMessage
from Planky.plankyData import PlankyData
from Planky.plankyServer import PlankyServer

server = PlankyServer("127.0.0.1", port=1111)

@server.on_message(ParsedMessage)
async def parsed_message(handler, event: MessageEvent):
    await handler.send_data(PlankyData(event.message.content))


def mainloop():
    server.mainloop()


if __name__ == "__main__": mainloop()

