from typing import List as _List
from pitica.table import Table as _Table
from pitica import constants as _constants
from pitica.filter import Filter as _Filter
from pitica.persistance.iengine import IEngine as _IEngine


class Dummy(_IEngine):
    def __init__(self,
                 host: str = _constants.DEFAULT_DB_HOST,
                 port: int = _constants.DEFAULT_DB_PORT,
                 user: str = None,
                 password: str = None,
                 database: str = _constants.DEFAULT_DB_NAME):
        return

    def check_database() -> bool:
        return True

    def create_database(database_schema: _List[_Table]) -> bool:
        return True

    def insert(self, table: str, data: dict) -> int:
        return None

    def update(self, table: str, id: str, data: dict) -> dict:
        return {}

    def delete(self, table: str, filters: _Filter) -> dict:
        return {}

    def select(self, table: str, filters: _Filter) -> dict:
        return {}

    def select_many2many(self, table: str, relation_table: str, target: str, target_id: str) -> dict:
        return {}
