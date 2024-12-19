from dataclasses import dataclass

from Planky.base.data.data import Data


@dataclass
class PlankyData(Data):
    """
    Default implementation of Data
    """
    payload: bytes
    '''
    payload for sending
    '''