from collections.abc import Callable

from Planky import listeners
from Planky.base.server import Server


class OnPing:
    def on_ping(self, filter: Callable = None):

        def decorator(func: Callable):
            if isinstance(self, Server):
                self.handler.add_listener(listeners.OnPing(func, filter))

        return decorator