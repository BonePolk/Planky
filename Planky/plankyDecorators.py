from Planky.decorators.onConnect import OnConnect
from Planky.decorators.onDisconnect import OnDisconnect
from Planky.decorators.onMessage import OnMessage
from Planky.decorators.onPing import OnPing


class PlankyDecorators(
    OnConnect,
    OnMessage,
    OnPing,
    OnDisconnect
):
    pass