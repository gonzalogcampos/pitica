import os as _os
import logging as _logging
from enum import Enum as _Enum
from threading import Lock as _Lock

from pitica import constants as _constants
from pitica.table import Table as _Table
from pitica.filter import Filter as _Filter
from pitica.config_reader import ConfigReader as _ConfigReader
from pitica.persistance.iengine import IEngine as _IEngine
from pitica.persistance.engines.mysql_engine import MySql as _MySql
from pitica.persistance.engines.dummy import Dummy as _Dummy

_logger = _logging.getLogger(__name__)
_lock = _Lock()


class Persistance:
    class Engines(_Enum):
        MYSQL = _MySql
        DUMMY = _Dummy

    def __init__(self,
                 root_dir: str = None,
                 host: str = _constants.DEFAULT_DB_HOST,
                 port: int = _constants.DEFAULT_DB_PORT,
                 user: str = None,
                 password: str = None,
                 database: str = _constants.DEFAULT_DB_NAME,
                 engine: Engines = Engines.DUMMY):

        self._database: _IEngine = engine.value(host=host,
                                                port=port,
                                                user=user,
                                                password=password,
                                                database=database)
        self._enabled: bool = True
        self._check_database(root_dir)

    def _check_database(self, root_dir: str) -> bool:

        if not root_dir:
            _logger.debug(
                f"Not root directory provided. Avoiding database check.")
            return False

        _logger.debug(f"Checking database exists")
        if self._database.check_database():
            return True

        config_schema = _ConfigReader(_os.path.join(
            root_dir, _constants.SCHEMA_FILENAME)).get_config()
        tables = _Table.create_tables(config_schema)
        _logger.debug(f"Creating database tables")
        self._database.create_database(tables)

    def insert(self, table: str, data: dict) -> int:
        if not self._enabled:
            return None
        with _lock:
            _logger.debug(f"Inserting in {table} | {data}")
            result = self._database.insert(table=table, data=data)
        return result

    def update(self, table: str, id: str, data: dict) -> dict:
        if not self._enabled:
            return None
        with _lock:
            _logger.debug(f"Updating in {table} {id} | {data}")
            result = self._database.update(table=table, id=id, data=data)
        return result

    def delete(self, table: str, filters: _Filter) -> dict:
        if not self._enabled:
            return None
        with _lock:
            _logger.debug(
                f"Deleting in {table} | {str(filters)}")
            result = self._database.delete(table=table, filters=filters)
        return result

    def select(self, table: str, filters: _Filter) -> dict:
        if not self._enabled:
            return None
        with _lock:
            _logger.debug(f"Selecting in {table} | {str(filters)}")
            result = self._database.select(table=table, filters=filters)
        return result

    def select_many2many(self, table: str, relation_table: str, target: str, target_id: str):
        if not self._enabled:
            return None
        with _lock:
            _logger.debug(f"Selecting from relation table {relation_table}")
            result = self._database.select_many2many(
                table, relation_table, target, target_id)
        return result

    def enable(self, value: bool) -> None:
        self._enabled = value
