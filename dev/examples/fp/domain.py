# Auto generated from Model SQL (c)
# Copyright Gonzalo G. Campos 2024

from typing import Self as _Self
from typing import List as _List
from datetime import datetime as _datetime
from pitica.entity import Entity as _Entity
from pitica.filter import Filter as _Filter
from pitica.filter import FilterOperator as _FilterOperator


class Domain(_Entity):
   def __init__(self):
      super().__init__(Domain)
      self._name = None
      self._paused = None
      self._state = None

   def get_name(self) -> str:
      return self._name

   def set_name(self, value: str) -> _Self:
      self._change('name', value)
      self._name = value
      return self

   def get_paused(self) -> bool:
      return self._paused

   def set_paused(self, value: bool) -> _Self:
      self._change('paused', value)
      self._paused = value
      return self

   def get_state(self) -> str:
      return self._state

   def set_state(self, value: str) -> _Self:
      self._change('state', value)
      self._state = value
      return self

   def get_module(self) -> _List[_Entity]:
      from .module import Module
      return self._select_many2many(Module, 'Domain_Module')

   def add_module(self, module: _Entity) -> _Self:
      self._add_many2many(module, 'Domain_Module')
      return self

   def remove_module(self, module: _Entity) -> _Self:
      self._remove_many2many(module, 'Domain_Module')
      return self

   def get_occurrence_domain(self) -> _List[_Entity]:
      from .occurrence import Occurrence
      filter = _Filter('domain', _FilterOperator.EQUALS, self.get_id())
      return Occurrence.find_all(filters=filter)

   def as_dict(self) -> dict:
      result = dict()
      result['id'] = self.get_id()
      result['name'] = self._name
      result['paused'] = self._paused
      result['state'] = self._state
      return result

   def _get_many2many_relations(self) -> _List[str]:
      relations = []
      relations.append('Domain_Module')
      return relations

   @staticmethod
   def find_by_name(name: str, filter_operator: _FilterOperator = _FilterOperator.EQUALS) -> _Self:
      filters = _Filter('name', filter_operator, name)
      all = Domain.find_all(filters=filters)
      if all:
         return all[0]
      return None

   @staticmethod
   def find_by_paused(paused: bool, filter_operator: _FilterOperator = _FilterOperator.EQUALS) -> _Self:
      filters = _Filter('paused', filter_operator, paused)
      all = Domain.find_all(filters=filters)
      return all

   @staticmethod
   def find_by_state(state: str, filter_operator: _FilterOperator = _FilterOperator.EQUALS) -> _Self:
      filters = _Filter('state', filter_operator, state)
      all = Domain.find_all(filters=filters)
      return all

