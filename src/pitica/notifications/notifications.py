import json as _json
from typing import Set as _Set
from typing import Dict as _Dict
from typing import List as _List
import logging as _logging
from enum import Enum as _Enum
from typing import Callable as _Callable

from pitica import constants as _constants
from pitica.notifications.iengine import IEngine as _IEngine
from pitica.notifications.engines.redis_ps import RedisPS as _RedisPS
from pitica.notifications.engines.redis_client import Redis as _Redis
from pitica.notifications.engines.dummy import Dummy as _Dummy

_logger = _logging.getLogger(__name__)

_NOTIFICATION_TYPE_KEY = "notification_type"
_NOTIFICATION_DATA_KEY = "notification_data"


class Notifications():
    class Engines(_Enum):
        REDIS = _Redis
        REDIS_PS = _RedisPS
        DUMMY = _Dummy

    class Type(_Enum):
        CREATION = "CREATE"
        EDITION = "EDIT"
        DELETION = "DELETE"

    class _callback:
        def __init__(self,
                     id: int,
                     entity: str,
                     notification_type: str,
                     function: _Callable[[str, dict], None]):
            self.id: int = id
            self.entity: str = entity
            self.notification_type: str = notification_type
            self.function: _Callable[[str, dict], None] = function
            self.enabled: bool = True

    def __init__(self,
                 host: str = _constants.DEFAULT_NOTIFICATION_HOST,
                 port: str = _constants.DEFAULT_NOTIFICATION_PORT,
                 id: str = None,
                 engine: Engines = Engines.DUMMY):

        self._engine: _IEngine = engine.value(
            host, port, callback=self._notification, id=id)
        self._callbacks: _Dict[str,
                               _Dict[str, _List[Notifications._callback]]] = {}
        self._next_id: int = 0
        self._enabled: bool = True

    def notify(self, classname: str, notification_type: Type, notification_data: dict) -> bool:
        if not self._enabled:
            return None
        key = classname
        data = {_NOTIFICATION_TYPE_KEY: notification_type.value,
                _NOTIFICATION_DATA_KEY: notification_data}
        data = _json.dumps(data)
        _logger.debug(
            f"Notifying {classname} {notification_type.value} | {notification_data}")
        if not notification_data:
            _logger.warn(
                "Notification of empty data for {classname} {notification_type.value}")
        return self._engine.add(key, data)

    def add_listener(self, notification_type: Type, entities: _Set[type], callback: _Callable[[str, dict], None]) -> int:
        id = self._next_id
        self._next_id += 1

        notification_type = notification_type.value

        if not self._callbacks:
            self._engine.start_listening()
            _logger.debug("Started listening notifications")

        for entity in entities:
            entity_name = entity.__name__
            if entity_name not in self._callbacks:
                self._callbacks[entity_name] = {}

            if notification_type not in self._callbacks[entity_name]:
                self._callbacks[entity_name][notification_type] = []

            callback_obj = Notifications._callback(
                id, entity_name, notification_type, callback)
            self._callbacks[entity_name][notification_type].append(
                callback_obj)

        _logger.debug(
            f"Listener {id} added for {notification_type} [{', '.join([e.__name__ for e in entities])}]")
        return id

    def set_enable_listener(self, id: int, enable: bool) -> None:
        for entity in list(self._callbacks.keys()):
            for nt in list(self._callbacks[entity].keys()):
                for callback in self._callbacks[entity][nt]:
                    if callback.id == id:
                        callback.enabled = enable

    def remove_listener(self, id: int) -> None:
        for entity in list(self._callbacks.keys()):
            for nt in list(self._callbacks[entity].keys()):
                self._callbacks[entity][nt] = [
                    i for i in self._callbacks[entity][nt] if i.id != id]
                if not self._callbacks[entity][nt]:
                    self._callbacks[entity].pop(nt)
            if not self._callbacks[entity]:
                self._callbacks.pop(entity)

        _logger.debug(f"Listener {id} removed")

        if not self._callbacks:
            self._engine.stop_listening()
            _logger.debug("Stopped listening notifications")

    def _notification(self, key: str, data: str):
        _logger.debug(f"Notification received for {key} | {data}")
        notification_dict = _json.loads(data)
        notification_type = notification_dict[_NOTIFICATION_TYPE_KEY]
        notification_data = notification_dict[_NOTIFICATION_DATA_KEY]

        callbacks: list[Notifications._callback] = self._callbacks.get(
            key, {}).get(notification_type) or []

        for callback in callbacks:
            if not callback.enabled:
                continue

            callback.function(key, notification_data)

    def enable(self, value: bool) -> None:
        self._enabled = value
