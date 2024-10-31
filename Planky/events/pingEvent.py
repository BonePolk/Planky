from dataclasses import dataclass

from Planky.base.data.event import Event

@dataclass
class ConnectEvent(Event):
    client_ip: str
    client_port: int
