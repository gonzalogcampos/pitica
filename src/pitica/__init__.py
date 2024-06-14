from enum import Enum as _Enum
from typing import Callable as _Callable
from typing import Set as _Set

from pitica import constants as _constants
from pitica.persistance.persistance import Persistance as _Persistance
from pitica.notifications.notifications import Notifications as _Notifications


class PersistanceEngine(_Enum):
    MYSQL = _Persistance.Engines.MYSQL.value
    DUMMY = _Persistance.Engines.DUMMY.value


class NotificationsEngine(_Enum):
    REDIS = _Notifications.Engines.REDIS.value
    REDIS_PS = _Notifications.Engines.REDIS_PS.value
    DUMMY = _Notifications.Engines.DUMMY.value


class NotificationType(_Enum):
    CREATION = _Notifications.Type.CREATION.value
    DELETION = _Notifications.Type.DELETION.value
    EDITION = _Notifications.Type.EDITION.value


_PERSISTANCE: _Persistance = _Persistance(
    engine=PersistanceEngine.DUMMY)
_NOTIFICATIONS: _Notifications = _Notifications(
    engine=NotificationsEngine.DUMMY)


def setup_persistance(root_dir: str = None,
                      host: str = _constants.DEFAULT_DB_HOST,
                      port: int = _constants.DEFAULT_DB_PORT,
                      user: str = None,
                      password: str = None,
                      database: str = _constants.DEFAULT_DB_NAME,
                      engine: PersistanceEngine = PersistanceEngine.MYSQL) -> None:
    global _PERSISTANCE
    _PERSISTANCE = _Persistance(root_dir,
                                host=host,
                                port=port,
                                user=user,
                                password=password,
                                database=database,
                                engine=engine)


def setup_notifications(host: str = _constants.DEFAULT_NOTIFICATION_HOST,
                        port: int = _constants.DEFAULT_NOTIFICATION_PORT,
                        id: str = None,
                        engine: NotificationsEngine = NotificationsEngine.REDIS_PS) -> None:
    global _NOTIFICATIONS
    _NOTIFICATIONS = _Notifications(
        host=host, port=port, id=id, engine=engine)


def get_repository() -> _Persistance:
    return _PERSISTANCE


def get_notifications() -> _Notifications:
    return _NOTIFICATIONS


def add_listener(notification_type: NotificationType,
                 entities: _Set[type],
                 callback: _Callable[[str, dict], None]) -> int:
    return get_notifications().add_listener(notification_type, entities, callback)


def disable_listener(id: int) -> None:
    return get_notifications().set_enable_listener(id, False)


def enable_listener(id: int) -> None:
    return get_notifications().set_enable_listener(id, True)


def remove_listener(id: int) -> None:
    return get_notifications().remove_listener(id)


def enable_persistance() -> None:
    get_repository().enable(True)


def disable_persistance() -> None:
    get_repository().enable(False)


def enable_notifications() -> None:
    get_notifications().enable(True)


def disable_notifications() -> None:
    get_notifications().enable(False)
