from collections.abc import Callable


class Listener:
    def __init__(self, callback: Callable, filter: Callable):
        self.callback = callback
        self.filter = filter

    async def check_event(self, event, handler):
        if not self.filter or self.filter(event): await self.callback(handler, event)