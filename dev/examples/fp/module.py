# Auto generated from Model SQL (c)
# Copyright Gonzalo G. Campos 2024

from typing import Self as _Self
from typing import List as _List
from datetime import datetime as _datetime
from pitica.entity import Entity as _Entity
from pitica.filter import Filter as _Filter
from pitica.filter import FilterOperator as _FilterOperator


class Module(_Entity):
   def __init__(self):
      super().__init__(Module)
      self._name = None

   def get_name(self) -> str:
      return self._name

   def set_name(self, value: str) -> _Self:
      self._change('name', value)
      self._name = value
      return self

   def get_domain(self) -> _List[_Entity]:
      from .domain import Domain
      return self._select_many2many(Domain, 'Domain_Module')

   def add_domain(self, domain: _Entity) -> _Self:
      self._add_many2many(domain, 'Domain_Module')
      return self

   def remove_domain(self, domain: _Entity) -> _Self:
      self._remove_many2many(domain, 'Domain_Module')
      return self

   def get_activity_module(self) -> _List[_Entity]:
      from .activity import Activity
      filter = _Filter('module', _FilterOperator.EQUALS, self.get_id())
      return Activity.find_all(filters=filter)

   def as_dict(self) -> dict:
      result = dict()
      result['id'] = self.get_id()
      result['name'] = self._name
      return result

   def _get_many2many_relations(self) -> _List[str]:
      relations = []
      relations.append('Domain_Module')
      return relations

   @staticmethod
   def find_by_name(name: str, filter_operator: _FilterOperator = _FilterOperator.EQUALS) -> _Self:
      filters = _Filter('name', filter_operator, name)
      all = Module.find_all(filters=filters)
      if all:
         return all[0]
      return None

