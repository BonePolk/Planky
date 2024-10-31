from dataclasses import dataclass


@dataclass
class Event:
    client_ip: str
    client_port: int



    