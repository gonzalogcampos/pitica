# Auto generated from Model SQL (c)
# Copyright Gonzalo G. Campos 2024

from typing import Self as _Self
from typing import List as _List
from datetime import datetime as _datetime
from pitica.entity import Entity as _Entity
from pitica.filter import Filter as _Filter
from pitica.filter import FilterOperator as _FilterOperator
from .domain import Domain
from .activity import Activity


class Occurrence(_Entity):
   def __init__(self):
      super().__init__(Occurrence)
      self._alias = None
      self._scheduled_id = None
      self._duration = None
      self._start = None
      self._started = None
      self._finished = None
      self._status = None
      self._compound_id = None
      self._domain = None
      self._activity = None

   def get_alias(self) -> str:
      return self._alias

   def set_alias(self, value: str) -> _Self:
      self._change('alias', value)
      self._alias = value
      return self

   def get_scheduled_id(self) -> str:
      return self._scheduled_id

   def set_scheduled_id(self, value: str) -> _Self:
      self._change('scheduled_id', value)
      self._scheduled_id = value
      return self

   def get_duration(self) -> int:
      return self._duration

   def set_duration(self, value: int) -> _Self:
      self._change('duration', value)
      self._duration = value
      return self

   def get_start(self) -> _datetime:
      return self._start

   def set_start(self, value: _datetime) -> _Self:
      if not isinstance(value, _datetime):
         value = _datetime.fromisoformat(value)
      self._change('start', value)
      self._start = value
      return self

   def get_started(self) -> _datetime:
      return self._started

   def set_started(self, value: _datetime) -> _Self:
      if not isinstance(value, _datetime):
         value = _datetime.fromisoformat(value)
      self._change('started', value)
      self._started = value
      return self

   def get_finished(self) -> _datetime:
      return self._finished

   def set_finished(self, value: _datetime) -> _Self:
      if not isinstance(value, _datetime):
         value = _datetime.fromisoformat(value)
      self._change('finished', value)
      self._finished = value
      return self

   def get_status(self) -> str:
      return self._status

   def set_status(self, value: str) -> _Self:
      self._change('status', value)
      self._status = value
      return self

   def get_compound_id(self) -> str:
      return self._compound_id

   def set_compound_id(self, value: str) -> _Self:
      self._change('compound_id', value)
      self._compound_id = value
      return self

   def get_domain(self) -> Domain:
      return Domain.find_by_id(self._domain)

   def set_domain(self, domain: Domain) -> _Self:
      self._change('domain', domain.get_id())
      self._domain = domain.get_id()
      return self

   def get_activity(self) -> Activity:
      return Activity.find_by_id(self._activity)

   def set_activity(self, activity: Activity) -> _Self:
      self._change('activity', activity.get_id())
      self._activity = activity.get_id()
      return self

   def as_dict(self) -> dict:
      result = dict()
      result['id'] = self.get_id()
      result['alias'] = self._alias
      result['scheduled_id'] = self._scheduled_id
      result['duration'] = self._duration
      result['start'] = self._start.isoformat()
      result['started'] = self._started.isoformat()
      result['finished'] = self._finished.isoformat()
      result['status'] = self._status
      result['compound_id'] = self._compound_id
      result['domain'] = self._domain
      result['activity'] = self._activity
      return result

   def _get_many2many_relations(self) -> _List[str]:
      relations = []
      return relations

   @staticmethod
   def find_by_alias(alias: str, filter_operator: _FilterOperator = _FilterOperator.EQUALS) -> _Self:
      filters = _Filter('alias', filter_operator, alias)
      all = Occurrence.find_all(filters=filters)
      return all

   @staticmethod
   def find_by_scheduled_id(scheduled_id: str, filter_operator: _FilterOperator = _FilterOperator.EQUALS) -> _Self:
      filters = _Filter('scheduled_id', filter_operator, scheduled_id)
      all = Occurrence.find_all(filters=filters)
      return all

   @staticmethod
   def find_by_duration(duration: int, filter_operator: _FilterOperator = _FilterOperator.EQUALS) -> _Self:
      filters = _Filter('duration', filter_operator, duration)
      all = Occurrence.find_all(filters=filters)
      return all

   @staticmethod
   def find_by_start(start: _datetime, filter_operator: _FilterOperator = _FilterOperator.EQUALS) -> _Self:
      filters = _Filter('start', filter_operator, start)
      all = Occurrence.find_all(filters=filters)
      return all

   @staticmethod
   def find_by_started(started: _datetime, filter_operator: _FilterOperator = _FilterOperator.EQUALS) -> _Self:
      filters = _Filter('started', filter_operator, started)
      all = Occurrence.find_all(filters=filters)
      return all

   @staticmethod
   def find_by_finished(finished: _datetime, filter_operator: _FilterOperator = _FilterOperator.EQUALS) -> _Self:
      filters = _Filter('finished', filter_operator, finished)
      all = Occurrence.find_all(filters=filters)
      return all

   @staticmethod
   def find_by_status(status: str, filter_operator: _FilterOperator = _FilterOperator.EQUALS) -> _Self:
      filters = _Filter('status', filter_operator, status)
      all = Occurrence.find_all(filters=filters)
      return all

   @staticmethod
   def find_by_compound_id(compound_id: str, filter_operator: _FilterOperator = _FilterOperator.EQUALS) -> _Self:
      filters = _Filter('compound_id', filter_operator, compound_id)
      all = Occurrence.find_all(filters=filters)
      return all

