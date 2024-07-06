from datetime import datetime as _datetime
import logging as _logging
import mysql.connector as _connector
from typing import List as _List
from pitica.table import Table as _Table
from pitica import constants as _constants
from pitica.filter import Filter as _Filter
from pitica.filter import FilterOperator as _FilterOperator
from pitica.persistance.iengine import IEngine as _IEngine

_logger = _logging.getLogger(__name__)

_TYPES_CONVERSION = {
    float: "float",
    int: "int",
    bool: "bool",
    str: "varchar(255)",
    _datetime: "datetime(3)",
    _constants.ID_ATTRIBUTE: "MEDIUMINT"
}

_VALUES_MAPPER = {
    float: lambda d: f"{float(d)}",
    int: lambda d: f"{int(d)}",
    bool: lambda d: f"{int(bool(d))}",
    str: lambda d: f"'{str(d)}'",
    type(None): lambda d: "NULL",
    _datetime: lambda d: f"'{d.isoformat()}'",
    _constants.ID_ATTRIBUTE: lambda d: f"{int(d)}"
}

_EXP_CONVERSION = {
    _FilterOperator.EQUALS: "=",
    _FilterOperator.NOT_EQUALS: "!=",
    _FilterOperator.IS: "IS",
    _FilterOperator.IS_NOT: "IS NOT",
    _FilterOperator.LESS: "<",
    _FilterOperator.LESS_OR_EQUAL: "<=",
    _FilterOperator.GREATER: ">",
    _FilterOperator.GREATER_OR_EQUAL: ">=",
    _FilterOperator.AND: "AND",
    _FilterOperator.OR: "OR"
}


class MySql(_IEngine):
    def __init__(self,
                 host: str = _constants.DEFAULT_DB_HOST,
                 port: int = _constants.DEFAULT_DB_PORT,
                 user: str = None,
                 password: str = None,
                 database: str = _constants.DEFAULT_DB_NAME):
        self._database = database

        self._mysql = _connector.connect(host=host,
                                         port=port,
                                         user=user,
                                         password=password)

    def create_database(self, database_schema: _List[_Table]) -> bool:
        self._create_database()

        try:
            self._reconnect()
        except Exception as err:
            self._drop_database()
            msg = f"Unable to connect to {self._database} database"
            _logger.error(msg)
            raise Exception(msg)

        for table in database_schema:
            try:
                self._create_table(table)
            except Exception as err:
                self._drop_database()
                msg = f"Unable to create table {table.name}"
                _logger.error(msg)
                _logger.error(err)
                raise Exception(msg)

        return True

    def check_database(self) -> bool:
        cursor = self._mysql.cursor()
        cursor.execute("SHOW DATABASES")
        for database in cursor:
            if database[0] == self._database:
                self._reconnect()
                return True
        return False

    def insert(self, table: str, data: dict) -> int:
        keys = []
        values = []
        for key, value in data.items():
            if value is None:
                continue
            keys.append(str(key))
            values.append(
                f"{str(_VALUES_MAPPER.get(value.__class__, lambda d: d)(value))}")
        keys = ", ".join(keys)
        values = ", ".join(values)
        query = f"INSERT INTO {table} ({keys}) VALUES ({values});"
        cursor = self._mysql.cursor()
        cursor.execute(query)
        self._mysql.commit()
        return cursor.lastrowid

    def update(self, table: str, id: str, data: dict) -> dict:
        if not data:
            return
        values = []
        for key, value in data.items():
            values.append(
                f"{str(key)} = {str(_VALUES_MAPPER.get(value.__class__, lambda d: d)(value))}")

        query = f"UPDATE {table} SET {', '.join(values)} WHERE {_constants.ID_ATTRIBUTE} = '{id}'"
        cursor = self._mysql.cursor()
        cursor.execute(query)
        self._mysql.commit()

    def delete(self, table: str, filters: _Filter) -> dict:
        filters_query = self._get_filter_query(filters)
        query = f"DELETE FROM {table}{filters_query}"
        cursor = self._mysql.cursor()
        cursor.execute(query)
        self._mysql.commit()

    def select(self, table: str, filters: _Filter) -> _List[dict]:
        filters_query = self._get_filter_query(filters)
        query = f"SELECT * FROM {table}{filters_query}"
        cursor = self._mysql.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        self._mysql.commit()
        column_names = cursor.column_names
        result_list = []
        for x in result:
            result_list.append(
                {column_names[index]: x[index] for index in range(len(column_names))})
        return result_list

    def select_many2many(self, table: str, relation_table: str, target: str, target_id: str) -> _List[dict]:
        query = f"SELECT {table}.* FROM {table}"
        query += f" INNER JOIN {relation_table}"
        query += f" ON {table}.{_constants.ID_ATTRIBUTE} = {relation_table}.{table}"
        query += f" INNER JOIN {target}"
        query += f" ON {target}.{_constants.ID_ATTRIBUTE} = {relation_table}.{target}"
        query += f" WHERE {target}.{_constants.ID_ATTRIBUTE} = {target_id}"

        cursor = self._mysql.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        self._mysql.commit()
        column_names = cursor.column_names
        result_list = []
        for x in result:
            result_list.append(
                {column_names[index]: x[index] for index in range(len(column_names))})
        return result_list

    def _reconnect(self):
        self._mysql = _connector.connect(
            host=self._mysql.server_host,
            port=self._mysql.server_port,
            user=self._mysql.user,
            password=self._mysql._password,
            database=self._database
        )

    def _get_filter_query(self, filters: _Filter) -> str:
        if not filters:
            return ""

        def recursive_function(filters: _Filter):
            filters_query = []
            for item in filters.get_representation():
                if isinstance(item, tuple):
                    c = "'" if isinstance(item[2], str) else ""
                    filters_query.append(
                        f"( {item[0]}{_EXP_CONVERSION[item[1]]}{c}{item[2]}{c} )")
                elif isinstance(item, list):
                    filters_query.append(f"( {recursive_function(item)} )")
                elif isinstance(item, _FilterOperator):
                    filters_query
            return " ".join(filters_query)
        filter_str = recursive_function(filters)
        return f" WHERE {filter_str}" if filter_str else ""

    def _create_database(self) -> None:
        _logger.debug(f"Creating {self._database} database")
        cursor = self._mysql.cursor()
        cursor.execute(f"CREATE DATABASE {self._database}")
        self._mysql.commit()

    def _drop_database(self) -> None:
        _logger.debug(f"Removing {self._database} database")
        cursor = self._mysql.cursor()
        cursor.execute(f"DROP DATABASE {self._database}")
        self._mysql.commit()

    def _create_table(self, table: _Table) -> None:
        _logger.debug(f"Creating {table.name} table")

        attributes = []
        for attribute in table.attributes:
            attribute_quey = f"{attribute.name} "
            attribute_quey += _TYPES_CONVERSION[attribute.attr_type]
            if attribute.mandatory:
                attribute_quey += " NOT NULL"
            if attribute.unique:
                attribute_quey += " UNIQUE"
            if attribute.name == _constants.ID_ATTRIBUTE:
                attribute_quey += " AUTO_INCREMENT"
            attributes.append(attribute_quey)

        relations = []
        for relation in table.relations:
            relations.append(
                f"FOREIGN KEY ({relation.attribute.name}) REFERENCES {relation.target_attribute.table.name}({relation.target_attribute.name})")

        attributes = f"{', '.join(attributes)}" if attributes else ""
        relations = f", {', '.join(relations)}" if relations else ""

        primary_key = f", PRIMARY KEY ({_constants.ID_ATTRIBUTE})"

        unique_key = ""
        table_attributes = [
            a.name for a in table.attributes if a.name != _constants.ID_ATTRIBUTE]
        if table.is_relation and len(table_attributes) == 2:
            unique_key = f", CONSTRAINT unique_pair UNIQUE KEY ({table_attributes[1]},{table_attributes[0]})"

        query = f"CREATE TABLE {table.name}({attributes}{relations}{primary_key}{unique_key})"

        cursor = self._mysql.cursor()
        cursor.execute(query)
        self._mysql.commit()
