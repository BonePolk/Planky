from dataclasses import dataclass

from Planky.base.data.data import Data


@dataclass
class PlankyData(Data):
    payload: bytes