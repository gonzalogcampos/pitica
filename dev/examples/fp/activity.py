# Auto generated from Model SQL (c)
# Copyright Gonzalo G. Campos 2024

from typing import Self as _Self
from typing import List as _List
from datetime import datetime as _datetime
from pitica.entity import Entity as _Entity
from pitica.filter import Filter as _Filter
from pitica.filter import FilterOperator as _FilterOperator
from .module import Module


class Activity(_Entity):
   def __init__(self):
      super().__init__(Activity)
      self._name = None
      self._module = None

   def get_name(self) -> str:
      return self._name

   def set_name(self, value: str) -> _Self:
      self._change('name', value)
      self._name = value
      return self

   def get_module(self) -> Module:
      return Module.find_by_id(self._module)

   def set_module(self, module: Module) -> _Self:
      self._change('module', module.get_id())
      self._module = module.get_id()
      return self

   def get_occurrence_activity(self) -> _List[_Entity]:
      from .occurrence import Occurrence
      filter = _Filter('activity', _FilterOperator.EQUALS, self.get_id())
      return Occurrence.find_all(filters=filter)

   def as_dict(self) -> dict:
      result = dict()
      result['id'] = self.get_id()
      result['name'] = self._name
      result['module'] = self._module
      return result

   def _get_many2many_relations(self) -> _List[str]:
      relations = []
      return relations

   @staticmethod
   def find_by_name(name: str, filter_operator: _FilterOperator = _FilterOperator.EQUALS) -> _Self:
      filters = _Filter('name', filter_operator, name)
      all = Activity.find_all(filters=filters)
      if all:
         return all[0]
      return None

