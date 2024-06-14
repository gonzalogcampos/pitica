import redis as _redis
from threading import Thread as _Thread
from typing import Callable as _Callable
from datetime import datetime as _datetime

from pitica import constants as _constants
from pitica.notifications.iengine import IEngine as _IEngine


class RedisPS(_IEngine):
    def __init__(self,
                 host: str,
                 port: str,
                 callback: _Callable[[str, str], None],
                 id: str = None,
                 user: str = None,
                 password: str = None):
        self._thread: _Thread = None
        self._stop_thread: bool = True
        self._callback: _Callable[[str, str], None] = callback

        self._redis = _redis.StrictRedis(host=host, port=port, db=0)
        self._channel: str = _constants.NAME.encode('UTF-8')

    def __del__(self):
        self.stop_listening()

    def add(self, key: str, value: str) -> int:
        self._redis.publish(self._channel, str((key, value)))

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
        pubsub: _redis.client.PubSub = self._redis.pubsub()
        pubsub.subscribe(self._channel)
        for message in pubsub.listen():
            if message['type'] != 'message':
                continue

            message = message['data'].decode('utf-8')
            key, data = eval(message)
            self._callback(key, data)

            if self._stop_thread:
                pubsub.unsubscribe(self._channel)
                break
