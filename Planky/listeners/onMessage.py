from collections.abc import Callable
from typing import Type

from Planky.base.data.message import Message
from Planky.base.listener import Listener
from Planky.events.messageEvent import MessageEvent


class OnMessage(Listener):
    def __init__(self, func: Callable, msg_class: Type[Message], filter: Callable = None):
        super().__init__(func, filter)
        self.msg_class = msg_class

    async def check_event(self, event: MessageEvent, handler):
        if isinstance(event.message, self.msg_class):
            return await super().check_event(event, handler)