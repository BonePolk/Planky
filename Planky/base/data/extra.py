from dataclasses import dataclass


@dataclass
class Extra:
    client_ip: str
    client_port: int
