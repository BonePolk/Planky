from Planky.plankyServer import PlankyServer

server = PlankyServer("127.0.0.1", port=1111)

def mainloop():
    server.mainloop()

if __name__ == "__main__": mainloop()
