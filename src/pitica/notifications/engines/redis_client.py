import redis as _redis
from threading import Thread as _Thread
from typing import Callable as _Callable
from datetime import datetime as _datetime

from pitica import constants as _constants
from pitica.notifications.iengine import IEngine as _IEngine


class Redis(_IEngine):
    def __init__(self,
                 host: str,
                 port: str,
                 callback: _Callable[[str, str], None],
                 id: str = None,
                 user: str = None,
                 password: str = None):
        self._thread: _Thread = None
        self._stop_thread: bool = True
        self._stream: str = _constants.NAME.encode('UTF-8')
        self._consumer_group: str = f"{_constants.NAME}-{id}"
        self._consumer_name: int = 0
        self._callback: _Callable[[str, str], None] = callback
        self._redisCli = _redis.Redis(host=host, port=port)
        try:
            self._redisCli.execute_command(
                'XGROUP', 'CREATE', self._stream, self._consumer_group, '$', 'MKSTREAM')
        except _redis.exceptions.ResponseError as err:
            pass

    def __del__(self):
        self.stop_listening()

    def add(self, key: str, value: str) -> int:
        self._redisCli.xadd(self._stream, {key: value})

    def start_listening(self) -> None:
        if not self._thread:
            self._thread = _Thread(target=self._thread_function)
            self._consumer_name = int(round(_datetime.now().timestamp()))
            self._stop_thread = False
            self._thread.start()

    def stop_listening(self) -> None:
        self._stop_thread = True
        self._thread = None

    def _thread_function(self):
        while True:
            messages = self._redisCli.xreadgroup(
                self._consumer_group, self._consumer_name, {self._stream: '>'})
            for stream, stream_data in messages or []:
                if stream != self._stream:
                    continue

                for id, event in stream_data:
                    for key, data in event.items():
                        self._callback(key.decode(), data.decode())

            if self._stop_thread:
                break
