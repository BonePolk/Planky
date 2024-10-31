from Planky.plankyServer import PlankyServer

server = PlankyServer("127.0.0.1", port=1112)
server.load_server_cert("public.pem", "private.pem")

def mainloop():
    server.mainloop()


if __name__ == "__main__": mainloop()

