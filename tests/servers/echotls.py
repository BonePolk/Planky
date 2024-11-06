from Planky.events.messageEvent import MessageEvent
from Planky.messages.parsedMessage import ParsedMessage
from Planky.plankyData import PlankyData
from Planky.plankyServer import PlankyServer

server = PlankyServer("127.0.0.1", port=1112)
server.load_server_cert("public.pem", "private.pem")

@server.on_message(ParsedMessage)
async def parsed_message(client, event: MessageEvent):
    print(event)
    await client.send_data(PlankyData(event.message.content))


def mainloop():
    server.mainloop()


if __name__ == "__main__": mainloop()

