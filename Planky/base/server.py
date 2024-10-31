class Server:
    def __init__(self, host: str, port: int=1111):
        self.connected = False
        self.handler = None

    def load_server_cert(self, cert_path: str, key_path: str, password: str = None): raise NotImplementedError
    def add_trusted_ca(self, ca_path: str): raise NotImplementedError
    def start(self): raise NotImplementedError
    async def mainloop(self): raise NotImplementedError