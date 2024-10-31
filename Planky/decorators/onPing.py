from collections.abc import Callable

from Planky import listeners
from Planky.base.server import Server


class OnPing:
    def on_ping(self, filter: Callable = None):
        """
        **Decorator!** Register callback on ping event

        :param filter: function to filter events
        """
        def decorator(func: Callable):
            if isinstance(self, Server):
                self.handler.add_listener(listeners.OnPing(func, filter))

        return decorator