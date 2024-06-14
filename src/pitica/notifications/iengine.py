from abc import ABC as _ABC
from typing import Callable as _Callable
from abc import abstractmethod as _abstractmethod


class IEngine(_ABC):
    @_abstractmethod
    def __init__(self,
                 host: str,
                 port: str,
                 callback: _Callable[[str, str], None],
                 id: str = None,
                 user: str = None,
                 password: str = None):
        ...

    @_abstractmethod
    def add(self, key: str, value: str) -> bool:
        ...

    @_abstractmethod
    def start_listening(self) -> None:
        ...

    @_abstractmethod
    def stop_listening(self) -> None:
        ...
