from abc import ABC as _ABC
from abc import abstractmethod as _abstractmethod
from typing import List as _List
from pitica import constants as _constants
from pitica.filter import Filter as _Filter
from pitica.table import Table as _Table


class IEngine(_ABC):
    @_abstractmethod
    def __init__(self,
                 host: str = _constants.DEFAULT_DB_HOST,
                 port: int = _constants.DEFAULT_DB_PORT,
                 user: str = None,
                 password: str = None,
                 database: str = _constants.DEFAULT_DB_NAME):
        ...

    @_abstractmethod
    def check_database() -> bool:
        ...

    @_abstractmethod
    def create_database(database_schema: _List[_Table]) -> bool:
        ...

    @_abstractmethod
    def insert(self, table: str, data: dict) -> int:
        ...

    @_abstractmethod
    def update(self, table: str, id: str, data: dict) -> dict:
        ...

    @_abstractmethod
    def delete(self, table: str, filters: _Filter) -> dict:
        ...

    @_abstractmethod
    def select(self, table: str, filters: _Filter) -> dict:
        ...

    @_abstractmethod
    def select_many2many(self, table: str, relation_table: str, target: str, target_id: str) -> dict:
        ...
