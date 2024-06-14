from typing import Callable as _Callable

from pitica.notifications.iengine import IEngine as _IEngine


class Dummy(_IEngine):
    def __init__(self,
                 host: str,
                 port: str,
                 callback: _Callable[[str, str], None],
                 id: str = None,
                 user: str = None,
                 password: str = None):
        return

    def add(self, key: str, value: str) -> bool:
        return True

    def start_listening(self) -> None:
        return

    def stop_listening(self) -> None:
        return
