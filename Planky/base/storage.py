from time import time
from typing import Any

from Planky.base.data.storageItem import StorageItem


class ItemNotFound(Exception): pass
class ItemExpired(Exception): pass


class Storage:
    '''
    Storage class for extra client data
    '''

    def __init__(self):
        self._storage: dict[str, StorageItem] = {

        }

    def get(self, key: str):
        '''

        :param key: Key of storage item
        :return: Value saved in storage

        :raises ItemNotFound: If item not found
        :raises ItemExpired: If item expired
        '''
        if key not in self._storage:
            raise ItemNotFound(f"Item {key} not found")

        item = self._storage.get(key)

        if item.expiration < 0 or item.expiration >= time():
            return item.value
        else:
            raise ItemExpired(f"Item {key} expired")

    def set(self, key: str, value: Any, lifetime: int = -1):
        '''

        :param key: Key for storage item
        :param value: Value of storage item
        :param lifetime: Lifetime of storage item
        _If >0 then object will raise ItemExpired after lifetime_

        :return:
        '''
        self._storage[key] = StorageItem(value, -1 if lifetime < 0 else time() + lifetime)


