import secrets
import socket
import ssl
import struct
import time
import unittest
from random import randint
from secrets import token_bytes
from threading import Thread
from time import sleep


def start_server(mainloop, server):
    Thread(target=mainloop).start()

    while not server.started:
        sleep(0.1)

def stop_server(server):
    try:
        server.stop()
    except TypeError as e:
        print("Server already stopped")


class ConnectionTestCase(unittest.TestCase):
    def test_ping(self):
        from tests.servers.tcpserver import server, mainloop
        start_server(mainloop, server)

        client_socket = socket.create_connection(("127.0.0.1", 1111))
        client_socket.settimeout(5)
        client_socket.send(struct.pack(">I", 0))
        data = client_socket.recv(4)

        try:
            server.stop()
        except:
            pass

        self.assertEqual(data, b"\x00\x00\x00\x00")

    def test_echo(self):
        from tests.servers.echotcp import server, mainloop
        start_server(mainloop, server)

        client_socket = socket.create_connection(("127.0.0.1", 1111))
        client_socket.settimeout(5)
        success = True
        timeout = False
        sent = None
        recved = None

        for _ in range(5):
            payload = token_bytes(randint(0, 128))
            sent = struct.pack(">I", len(payload)) + payload
            print(sent)
            client_socket.send(sent)

            try:
                recved = client_socket.recv(len(sent))
                if recved != sent:
                    break
            except TimeoutError as e:
                timeout = True
                break
            except Exception as e:
                print(str(e))
                break

        server.stop()
        if timeout: raise TimeoutError
        self.assertEqual(sent, recved)

    def test_hello(self):
        from tests.servers.hellotcp import server, mainloop
        start_server(mainloop, server)

        client_socket = socket.create_connection(("127.0.0.1", 1111))
        client_socket.settimeout(5)

        timeout = False
        payload = b"\x00parsed"
        excepted = struct.pack(">I", len(payload)) + payload
        recved = None

        try:
            client_socket.send(struct.pack(">I", len(payload)) + payload)
            recved = client_socket.recv(len(excepted))
            if recved != excepted: raise Exception

            payload = b"\x01hello"
            excepted = struct.pack(">I", len(b"\x01World!")) + b"\x01World!"
            client_socket.send(struct.pack(">I", len(payload)) + payload)
            recved = client_socket.recv(len(excepted))
            if recved != excepted: raise Exception

            t = time.time()
            payload = b"\x02"+struct.pack(">I", int(t))
            excepted_payload = b"\x02"+str(int(t)).encode()
            excepted = struct.pack(">I", len(excepted_payload)) + excepted_payload
            client_socket.send(struct.pack(">I", len(payload)) + payload)
            recved = client_socket.recv(len(excepted))
            if recved != excepted: raise Exception
        except TimeoutError as e: timeout = True
        except Exception as e: pass
        finally: server.stop()

        if timeout: raise TimeoutError

        self.assertEqual(excepted, recved)

    def test_echo_clients(self):
        from tests.servers.echotcp import server, mainloop
        start_server(mainloop, server)

        client_socket = socket.create_connection(("127.0.0.1", 1111))
        client_socket.settimeout(5)

        recved = b""

        for _ in range(5):
            client_socket.send(struct.pack(">I", 1)+b"I")
            recved = client_socket.recv(5)

            if recved != b"\x00\x00\x00\x01I":
                break

        client_socket2 = socket.create_connection(("127.0.0.1", 1111))
        client_socket2.settimeout(5)

        for _ in range(5):
            client_socket2.send(struct.pack(">I", 1)+b"I")
            recved = client_socket2.recv(5)

            if recved != b"\x00\x00\x00\x01I":
                break

            client_socket.send(struct.pack(">I", 1) + b"I")
            recved = client_socket.recv(5)

            if recved != b"\x00\x00\x00\x01I":
                break

        server.stop()

        self.assertEqual(b"\x00\x00\x00\x01I", recved)


class TlsConnectionTestCase(unittest.TestCase):
    def test_ssl_cert_pinning(self):
        from tests.servers.emptytls import server, mainloop
        start_server(mainloop, server)
        failed = False
        try:
            context = ssl.create_default_context()
            sock = socket.create_connection(("localhost", 1112))
            ssl_socket = context.wrap_socket(sock, server_hostname="test")
            ssl_socket.settimeout(5)
        except ssl.SSLCertVerificationError as e:
            failed = True
        server.stop()
        self.assertTrue(failed)

    def test_ping_with_tls(self):
        from tests.servers.tlsserver import server, mainloop
        start_server(mainloop, server)

        context = ssl.create_default_context()
        context.load_verify_locations("public.pem")
        context.check_hostname = False
        sock = socket.create_connection(("localhost", 1112))
        ssl_socket = context.wrap_socket(sock)
        ssl_socket.settimeout(5)

        ssl_socket.send(struct.pack(">I", 0))
        data = ssl_socket.recv(4)
        server.stop()
        self.assertEqual(data, b"\x00\x00\x00\x00")

    def test_echo_tls(self):
        from tests.servers.echotls import server, mainloop
        start_server(mainloop, server)

        context = ssl.create_default_context()
        context.load_verify_locations("public.pem")
        context.check_hostname = False
        sock = socket.create_connection(("localhost", 1112))
        ssl_socket = context.wrap_socket(sock)
        ssl_socket.settimeout(5)
        timeout = False
        sent = None
        recved = None

        for _ in range(5):
            payload = token_bytes(randint(0, 128))
            sent = struct.pack(">I", len(payload)) + payload
            print(sent)
            ssl_socket.send(sent)

            try:
                recved = ssl_socket.recv(len(sent))
                if recved != sent:
                    break
            except TimeoutError as e:
                timeout = True
                break
            except Exception as e:
                print(str(e))
                break

        server.stop()
        if timeout: raise TimeoutError
        self.assertEqual(sent, recved)

    def test_hello_tls(self):
        from tests.servers.hellotls import server, mainloop
        start_server(mainloop, server)

        context = ssl.create_default_context()
        context.load_verify_locations("public.pem")
        context.check_hostname = False
        sock = socket.create_connection(("localhost", 1112))
        ssl_socket = context.wrap_socket(sock)
        ssl_socket.settimeout(5)

        timeout = False
        payload = b"\x00parsed"
        excepted = struct.pack(">I", len(payload)) + payload
        recved = None

        try:
            ssl_socket.send(struct.pack(">I", len(payload)) + payload)
            recved = ssl_socket.recv(len(excepted))
            if recved != excepted: raise Exception

            payload = b"\x01hello"
            excepted = struct.pack(">I", len(b"\x01World!")) + b"\x01World!"
            ssl_socket.send(struct.pack(">I", len(payload)) + payload)
            recved = ssl_socket.recv(len(excepted))
            if recved != excepted: raise Exception

            t = time.time()
            payload = b"\x02"+struct.pack(">I", int(t))
            excepted_payload = b"\x02"+str(int(t)).encode()
            excepted = struct.pack(">I", len(excepted_payload)) + excepted_payload
            ssl_socket.send(struct.pack(">I", len(payload)) + payload)
            recved = ssl_socket.recv(len(excepted))
            if recved != excepted: raise Exception
        except TimeoutError as e: timeout = True
        except Exception as e: pass
        finally: server.stop()

        if timeout: raise TimeoutError

        self.assertEqual(excepted, recved)

    def test_echo_clients_tls(self):
        from tests.servers.echotls import server, mainloop
        start_server(mainloop, server)

        context = ssl.create_default_context()
        context.load_verify_locations("public.pem")
        context.check_hostname = False
        sock = socket.create_connection(("localhost", 1112))
        ssl_socket = context.wrap_socket(sock)
        ssl_socket.settimeout(5)

        recved = b""

        for _ in range(5):
            ssl_socket.send(struct.pack(">I", 1)+b"I")
            recved = ssl_socket.recv(5)

            if recved != b"\x00\x00\x00\x01I":
                break

        context2 = ssl.create_default_context()
        context2.load_verify_locations("public.pem")
        context2.check_hostname = False
        sock2 = socket.create_connection(("localhost", 1112))
        ssl_socket2 = context2.wrap_socket(sock2)
        ssl_socket2.settimeout(5)

        for _ in range(5):
            ssl_socket2.send(struct.pack(">I", 1)+b"I")
            recved = ssl_socket2.recv(5)

            if recved != b"\x00\x00\x00\x01I":
                break

            ssl_socket.send(struct.pack(">I", 1) + b"I")
            recved = ssl_socket.recv(5)

            if recved != b"\x00\x00\x00\x01I":
                break

        server.stop()

        self.assertEqual(b"\x00\x00\x00\x01I", recved)


class StorageTestCase(unittest.TestCase):
    def test_client_storage(self):
        from tests.servers.storagetcp import server, mainloop
        start_server(mainloop, server)

        client_socket = socket.create_connection(("127.0.0.1", 1111))
        client_socket.settimeout(5)


        payload = b"\x01"
        excepted = b"\x01NoToken"

        client_socket.send(struct.pack(">I", 1))
        client_socket.send(payload)
        data = client_socket.recv(4)
        length = struct.unpack(">I", data)[0]
        data = client_socket.recv(length)

        if data != excepted:
            self.assertEqual(excepted, data)

        token = secrets.token_hex(16)
        payload = b"\x00" + token.encode()


        client_socket.send(struct.pack(">I", len(payload)))
        client_socket.send(payload)

        payload = b"\x01"
        excepted = b"\x01"+token.encode()

        client_socket.send(struct.pack(">I", 1))
        client_socket.send(payload)
        data = client_socket.recv(4)
        length = struct.unpack(">I", data)[0]
        data = client_socket.recv(length)

        stop_server(server)

        self.assertEqual(data, excepted)

    def test_global_storage(self):
        from tests.servers.storagetcp import server, mainloop
        start_server(mainloop, server)

        client_socket = socket.create_connection(("127.0.0.1", 1111))
        client_socket.settimeout(5)


        payload = b"\x03"
        excepted = b"\x03NoSecret"

        client_socket.send(struct.pack(">I", 1))
        client_socket.send(payload)
        data = client_socket.recv(4)
        length = struct.unpack(">I", data)[0]
        data = client_socket.recv(length)

        if data != excepted:
            self.assertEqual(excepted, data)

        token = secrets.token_hex(16)
        payload = b"\x02" + token.encode()


        client_socket.send(struct.pack(">I", len(payload)))
        client_socket.send(payload)

        payload = b"\x03"
        excepted = b"\x03"+token.encode()

        client_socket.send(struct.pack(">I", 1))
        client_socket.send(payload)
        data = client_socket.recv(4)
        length = struct.unpack(">I", data)[0]
        data = client_socket.recv(length)

        stop_server(server)

        self.assertEqual(data, excepted)


if __name__ == '__main__':
    unittest.main()
