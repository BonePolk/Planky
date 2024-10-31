from collections.abc import Callable

from Planky import listeners
from Planky.base.server import Server


class OnDisconnect:
    def on_disconnect(self, filter: Callable = None) -> Callable:
        """
        **Decorator!** Register callback on disconnect event

        :param filter: function to filter events
        """
        def decorator(func: Callable) -> Callable:
            if isinstance(self, Server):
                self.handler.add_listener(listeners.OnDisconnect(func, filter))

            return func

        return decorator