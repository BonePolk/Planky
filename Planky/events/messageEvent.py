from dataclasses import dataclass

from Planky.base.data.event import Event
from Planky.base.data.message import Message


@dataclass
class MessageEvent(Event):
    message: Message
