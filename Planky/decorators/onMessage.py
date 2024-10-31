from collections.abc import Callable
from typing import Type

from Planky import listeners
from Planky.base.data.message import Message
from Planky.base.server import Server


class OnMessage:
    def on_message(self, msg_class: Type[Message], filter: Callable = None):
        """
        **Decorator!** Register callback on message event

        :param msg_class: filter message class
        :param filter: function to filter events
        """
        def decorator(func: Callable):
            if isinstance(self, Server):
                self.handler.add_listener(listeners.OnMessage(func, msg_class, filter))

        return decorator