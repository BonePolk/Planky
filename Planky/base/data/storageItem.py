from dataclasses import dataclass
from typing import Any


@dataclass
class StorageItem:
    value: Any
    expiration: int