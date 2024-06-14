import os as _os
import logging as _logging
from typing import List as _List
from pitica.table import Table as _Table
from pitica.table import Relation as _Relation
from pitica.generator.class_generator import ClassGenerator as _ClassGenerator

_logger = _logging.getLogger(__name__)


class Generator:
    def __init__(self, config: dict):
        self._classes: _List[_ClassGenerator] = self._create_classes(config)

    def _create_classes(self, config: dict):
        tables: _List[_Table] = _Table.create_tables(config)
        relation_tables: _List[_Table] = [
            table for table in tables if table.is_relation]
        generators = []
        for table in tables:
            if table.is_relation:
                continue

            current_relation_tables = []
            for relation_table in relation_tables:
                source = relation_table.relations[0].target_attribute.table
                target = relation_table.relations[1].target_attribute.table
                if table in [source, target]:
                    current_relation_tables.append(relation_table)

            external_relations = self._get_external_relations(table, tables)

            generators.append(_ClassGenerator(
                table, current_relation_tables, external_relations))
        return generators

    def _get_external_relations(self, table: _Table, tables: _List[_Table]) -> _List[_Relation]:
        relations = []
        for _table in tables:
            if _table.is_relation:
                continue
            for relation in _table.relations:
                if relation.target_attribute.table is table:
                    relations.append(relation)
        return relations

    def _copy_init(self, output_dir):
        _logger.debug("Generating __init__.py file")
        init_output = _os.path.join(output_dir, "__init__.py")
        with open(init_output, "x") as file:
            file.write("")

    def get_classes(self) -> _List[_ClassGenerator]:
        return self._classes

    def generate(self, output_dir):
        for class_generator in self._classes:
            class_generator.generate(output_dir)

        self._copy_init(output_dir)
