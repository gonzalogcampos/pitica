from __future__ import annotations as _annotations
from typing import List as _List
from typing import Tuple as _Tuple

from pitica import constants as _constants


class Attribute:
    def __init__(self, table: Table, name: str, attr_type: type, mandatory: bool, unique: bool):
        self.table = table
        self.name = name
        self.attr_type = attr_type
        self.mandatory = mandatory
        self.unique = unique


class Relation:
    def __init__(self, attribute: Attribute, target_attribute: Attribute, mandatory: bool, unique: bool):
        self.attribute = attribute
        self.target_attribute = target_attribute
        self.mandatory = mandatory
        self.unique = unique


class Table:
    def __init__(self, name: str):
        self.name: str = name
        self.attributes: _List[Attribute] = []
        self.relations: _List[Relation] = []
        self.is_relation: bool = False
        self.id: Attribute = self.add_attribute(
            _constants.ID_ATTRIBUTE, _constants.ID_ATTRIBUTE, True, True)

    def add_attribute(self, name: str, attr_type: type, mandatory: bool = False, unique: bool = False) -> Attribute:
        attribute = Attribute(self, name, attr_type, mandatory, unique)
        self.attributes.append(attribute)
        return attribute

    def add_relation(self, name: str, target_attribute: Attribute, mandatory: bool = False, unique: bool = False) -> Relation:
        attribute = self.add_attribute(
            name, _constants.ID_ATTRIBUTE, mandatory, unique)
        relation = Relation(attribute, target_attribute, mandatory, unique)
        self.relations.append(relation)
        return relation

    @staticmethod
    def create_tables(tables_dict: dict) -> _List[Table]:
        tables: _List[Table] = []
        relation_tables = []
        for table_name, table_data in Table._order_tables(tables_dict):
            table = Table(table_name)

            for attribute_name, attribute_info in table_data.items():
                if attribute_info[_constants.K_TYPE] != _constants.ATTRIBUTE:
                    continue
                if attribute_name in _constants.FORBIDDEN_ARGS:
                    raise Exception(
                        f"Attribute {attribute_name} is forbidden.")
                table.add_attribute(attribute_name,
                                    _constants.TYPES_CONVERSION[attribute_info[_constants.K_ATTRIBUTE_TYPE]],
                                    bool(attribute_info.get(
                                        _constants.K_MANDATORY, False)),
                                    bool(attribute_info.get(_constants.K_UNIQUE, False)))

            for relation_name, relation_info in table_data.items():
                if relation_info[_constants.K_TYPE] != _constants.RELATION:
                    continue
                if relation_name in _constants.FORBIDDEN_ARGS:
                    raise Exception(
                        f"Relation name {relation_name} is forbidden.")
                target_name = relation_info[_constants.K_RELATION_TARGET]
                if target_name == table_name:
                    target = [table]
                else:
                    target = [t for t in tables if t.name == target_name]
                if len(target) != 1:
                    raise Exception(
                        f"Unable to create a relation between {table_name} and {target_name}")
                target = target[0]
                relation_type = relation_info.get(
                    _constants.K_RELATION_TYPE, _constants.ONE2ONE)
                mandatory = relation_info.get(_constants.K_MANDATORY, False)
                if relation_type == _constants.ONE2ONE:
                    table.add_relation(
                        relation_name, target.id, mandatory, True)
                elif relation_type == _constants.ONE2MANY:
                    table.add_relation(
                        relation_name, target.id, mandatory, False)
                elif relation_type == _constants.MANY2MANY:
                    relation_tables.append(
                        Table._create_m2m_relation(table, target, relation_name))

            tables.append(table)
        return tables + relation_tables

    @staticmethod
    def _create_m2m_relation(source: Table, target: Table, relation_name: str) -> Table:
        table = Table(f"{source.name}_{relation_name}")
        table.add_relation(source.name, source.id, True, False)
        table.add_relation(relation_name, target.id, True, False)
        table.is_relation = True
        return table

    @staticmethod
    def _order_tables(tables_dict: dict) -> _List[dict]:
        ordered_tables = []
        all_tables = [(name, data) for name, data in tables_dict.items()]

        def get_relations(t: _Tuple[str, dict], ts: _List[_Tuple[str, dict]]):
            target_names = [v[_constants.K_RELATION_TARGET] for v in t[1].values(
            ) if v[_constants.K_TYPE] == _constants.RELATION]
            return [table for table in all_tables if table[0] in target_names]

        while len(ordered_tables) < len(all_tables):
            for current_table in all_tables:
                if current_table in ordered_tables:
                    continue
                for relation in get_relations(current_table, all_tables):
                    if relation not in ordered_tables and relation is not current_table:
                        break
                else:
                    ordered_tables.append(current_table)
        return ordered_tables
