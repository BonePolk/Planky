import asyncio
import ssl
from asyncio import CancelledError

from Planky.base.server import Server
from Planky.plankyDecorators import PlankyDecorators
from Planky.plankyHandler import PlankyHandler


class PlankyServer(Server, PlankyDecorators):
    """
    A Planky server
    """
    def __init__(self, host: str, port: int = 1111):
        super().__init__(host, port)

        self.ssl_ctx = None
        self.host = host
        self.port = port
        self.handler = PlankyHandler(self)
        self.server: asyncio.Server = None

    def load_server_cert(self, cert_path: str, key_path: str, password: str = None):
        """
        Load server certificate.

        _After loading the certificate, your server will use **TLS**._
        :param cert_path: Path to public certificate.
        :param key_path: Path to private key.
        :param password: Password to decrypt private key.
        """
        self.ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self.ssl_ctx.load_cert_chain(certfile=cert_path, keyfile=key_path, password=password)

    def add_trusted_ca(self, ca_path: str):
        """
        Load trusted CA certificate to verify client certificate.

        _You must load server certificate first via **load_server_cert**._

        _After loading the certificate, your client must use one of certificates from trusted CA._
        :param ca_path: Path to trusted CA certificate.
        """
        if not self.ssl_ctx: raise Exception("Server cert must be loaded first")
        self.ssl_ctx.load_verify_locations(cafile=ca_path)
        self.ssl_ctx.verify_mode = ssl.CERT_REQUIRED

    def mainloop(self):
        """
        Start the server and block the current thread until the server is stopped.
        """
        asyncio.run(self._start())

    async def _start(self):
        self.server = await asyncio.start_server(
            self.handler.handle_client,
            self.host,
            self.port,
            ssl=self.ssl_ctx
        )

        print(f"Server started on {self.host}:{self.port}")

        self.connected = True
        try:
            async with self.server: await self.server.serve_forever()
        except CancelledError as e: pass
        except Exception as e: quit(str(e))
        finally:
            self.connected = False

    def stop(self):
        """
        Stop the server.
        """
        self.server.close()


    @property
    def started(self):
        """
        True if the server is started
        """
        return self.connected