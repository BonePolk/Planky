from dataclasses import dataclass

from Planky.base.data.event import Event


@dataclass
class DisconnectEvent(Event):
    description: str
    code: int
