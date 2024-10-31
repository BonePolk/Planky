from dataclasses import dataclass
from enum import Enum


class MessageType(Enum):
    PING = 0
    RAW_MESSAGE = 1
    PARSED_MESSAGE = 2

@dataclass
class Message:
    content: bytes = b''