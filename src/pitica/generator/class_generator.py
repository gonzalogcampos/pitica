import os as _os
import logging as _logging
from typing import List as _List
from datetime import datetime as _datetime
from pitica import constants as _constants
from pitica.table import Table as _Table
from pitica.table import Attribute as _Attribute
from pitica.table import Relation as _Relation

_logger = _logging.getLogger(__name__)


class ClassGenerator:
    def __init__(self, table: _Table, relation_tables: _List[_Table], external_relations: _List[_Relation]):
        self._table = table
        self._relation_tables = relation_tables
        self._external_relations = external_relations

    def get_name(self) -> str:
        return self._table.name

    def get_attributes(self) -> _List[_Attribute]:
        return self._table.attributes

    def get_relations(self) -> _List[_Relation]:
        return self._table.relations

    def _get_docstring(self) -> _List[str]:
        lines = [
            "# Auto generated from Model SQL (c)",
            "# Copyright Gonzalo G. Campos 2024",
            ""
        ]
        return lines

    def _get_imports(self) -> _List[str]:
        lines = [
            "from typing import Self as _Self",
            "from typing import List as _List",
            "from datetime import datetime as _datetime",
            "from pitica.entity import Entity as _Entity",
            "from pitica.filter import Filter as _Filter",
            "from pitica.filter import FilterOperator as _FilterOperator",
        ]
        for relation in self.get_relations():
            target = relation.target_attribute.table.name
            lines.append(f"from .{self._lower(target)} import {target}")

        lines.append("")
        lines.append("")
        return lines

    def _get_classname(self) -> _List[str]:
        lines = [
            f"class {self.get_name()}(_Entity):"
        ]
        return lines

    def _get_init(self) -> _List[str]:
        lines = [
            "   def __init__(self):",
            f"      super().__init__({self.get_name()})"
        ]

        for attribute in self.get_attributes():
            if attribute.name == _constants.ID_ATTRIBUTE:
                continue
            lines += [
                f"      self._{attribute.name} = None"
            ]
        lines += [""]
        return lines

    def _get_getters_and_setters(self) -> _List[str]:
        lines = []
        for attribute in self.get_attributes():
            if attribute.name == _constants.ID_ATTRIBUTE:
                continue
            if attribute in [r.attribute for r in self.get_relations()]:
                continue

            if attribute.attr_type.__name__ == "datetime":
                lines += [
                    f"   def get_{attribute.name}(self) -> _datetime:",
                    f"      return self._{attribute.name}",
                    "",
                    f"   def set_{attribute.name}(self, value: _datetime) -> _Self:",
                    f"      if isinstance(value, str):",
                    f"         value = _datetime.fromisoformat(value)",
                    f"      self._change('{attribute.name}', value)",
                    f"      self._{attribute.name} = value",
                    f"      return self",
                    ""
                ]
            else:
                lines += [
                    f"   def get_{attribute.name}(self) -> {attribute.attr_type.__name__}:",
                    f"      return self._{attribute.name}",
                    "",
                    f"   def set_{attribute.name}(self, value: {attribute.attr_type.__name__}) -> _Self:",
                    f"      self._change('{attribute.name}', value)",
                    f"      self._{attribute.name} = value",
                    f"      return self",
                    ""
                ]
        return lines

    def _get_finds(self) -> _List[str]:
        lines = []
        for attribute in self.get_attributes():
            if attribute.name == _constants.ID_ATTRIBUTE:
                continue
            if attribute in [r.attribute for r in self.get_relations()]:
                continue

            attr_type = attribute.attr_type.__name__
            if attr_type == _datetime.__name__:
                attr_type = f"_{attr_type}"

            lines += [
                f"   @staticmethod",
                f"   def find_by_{attribute.name}({attribute.name}: {attr_type}, filter_operator: _FilterOperator = _FilterOperator.EQUALS) -> _Self:",
                f"      filters = _Filter('{attribute.name}', filter_operator, {attribute.name})",
                f"      all = {self._table.name}.find_all(filters=filters)",
            ]

            if attribute.unique:
                lines += [
                    f"      if all:",
                    f"         return all[0]",
                    f"      return None",
                    ""
                ]
            else:
                lines += [
                    f"      return all",
                    ""
                ]
        return lines

    def _get_relations_getters_and_setters(self):
        lines = []
        for relation in self.get_relations():
            target_name = relation.target_attribute.table.name
            relation_name = target_name[0].lower() + target_name[1:]
            lines += [
                f"   def get_{relation_name}(self) -> {target_name}:",
                f"      return {target_name}.find_by_id(self._{relation.attribute.name})",
                "",
                f"   def set_{relation_name}(self, {relation_name}: {target_name}) -> _Self:",
                f"      self._change('{relation.attribute.name}', {relation_name}.get_id())",
                f"      self._{relation.attribute.name} = {relation_name}.get_id()",
                f"      return self",
                "",
            ]
        return lines

    def _get_relation_tables_getters_and_setters(self):
        lines = []
        for table in self._relation_tables:
            for relation in table.relations:
                if relation.target_attribute.table != self._table:
                    target = relation.target_attribute.table
                    break
            else:
                continue

            table_name = table.name
            target_type = target.name
            target_name = target_type[0].lower() + target_type[1:]

            lines += [
                f"   def get_{target_name}(self) -> _List[_Entity]:",
                f"      from .{self._lower(target_type)} import {target_type}",
                f"      return self._select_many2many({target_type}, '{table_name}')",
                "",
                f"   def add_{target_name}(self, {target_name}: _Entity) -> _Self:",
                f"      self._add_many2many({target_name}, '{table_name}')",
                f"      return self",
                "",
                f"   def remove_{target_name}(self, {target_name}: _Entity) -> _Self:",
                f"      self._remove_many2many({target_name}, '{table_name}')",
                f"      return self",
                "",
            ]
        return lines

    def _get_external_relations_getters(self):
        lines = []
        for external_relation in self._external_relations:
            name = external_relation.attribute.table.name
            attribute = external_relation.attribute.name
            if external_relation.unique:
                lines += [
                    f"   def get_{self._lower(name)}_{attribute}(self) -> _Entity:",
                    f"      from .{self._lower(name)} import {name}",
                    f"      filter = _Filter('{attribute}', _FilterOperator.EQUALS, self.get_id())",
                    f"      result = {name}.find_all(filters=filter)",
                    f"      return result[0] if result else None",
                    f""
                ]
            else:
                lines += [
                    f"   def get_{self._lower(name)}_{attribute}(self) -> _List[_Entity]:",
                    f"      from .{self._lower(name)} import {name}",
                    f"      filter = _Filter('{attribute}', _FilterOperator.EQUALS, self.get_id())",
                    f"      return {name}.find_all(filters=filter)",
                    f""
                ]
        return lines

    def _get_remove_relations(self):
        lines = [
            f"   def _get_many2many_relations(self) -> _List[str]:",
            f"      relations = []"
        ]
        for table in self._relation_tables:
            lines.append(f"      relations.append('{table.name}')")
            break
        lines += [
            f"      return relations",
            f""
        ]
        return lines

    def _get_dict(self):
        lines = [
            f"   def as_dict(self) -> dict:",
            f"      result = dict()"
        ]
        for attribute in self.get_attributes():
            if attribute.name == _constants.ID_ATTRIBUTE:
                lines.append(
                    f"      result['{attribute.name}'] = self.get_id()")
            else:
                if attribute.attr_type == _datetime:
                    lines.append(
                        f"      result['{attribute.name}'] = self._{attribute.name}.isoformat() if self._{attribute.name} else None")
                else:
                    lines.append(
                        f"      result['{attribute.name}'] = self._{attribute.name}")

        lines += [
            f"      return result",
            ""
        ]
        return lines

    def _get_functions(self):
        lines = self._get_getters_and_setters()
        lines += self._get_relations_getters_and_setters()
        lines += self._get_relation_tables_getters_and_setters()
        lines += self._get_external_relations_getters()
        lines += self._get_dict()
        lines += self._get_remove_relations()
        lines += self._get_finds()
        return lines

    def _generate_lines(self):
        lines = self._get_docstring()
        lines += self._get_imports()
        lines += self._get_classname()
        lines += self._get_init()
        lines += self._get_functions()
        return lines

    def _lower(self, name: str) -> str:
        return name[0].lower() + name[1:]

    def generate(self, output_dir):
        if not _os.path.exists(output_dir):
            _logger.debug(f"Creating directory: {output_dir}")
            _os.makedirs(output_dir)

        filename = self._lower(self.get_name())
        output_filepath = _os.path.join(output_dir, f"{filename}.py")

        if _os.path.exists(output_filepath):
            _logger.debug(f"Removing file: {_os.path.basename(output_dir)}")
            _os.remove(output_filepath)

        lines = []
        for line in self._generate_lines():
            lines.append(line)
            lines.append("\n")

        _logger.debug(f"Generating file: {_os.path.basename(output_dir)}")

        with open(output_filepath, "x") as file:
            file.writelines(lines)
