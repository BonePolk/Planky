from dataclasses import dataclass

from Planky.base.data.message import Message


@dataclass
class PingMessage(Message):
    pass
