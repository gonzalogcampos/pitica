# Auto generated from Model SQL (c)
# Copyright Gonzalo G. Campos 2024

from typing import Self as _Self
from pitica.entity import Entity as _Entity
from pitica.filter import Filter as _Filter
from pitica.filter import FilterOperator as _FilterOperator
from .person import Person


class Student(_Entity):
   def __init__(self):
      super().__init__(Student)
      self._person = None

   def get_person(self) -> Person:
      return Person.find_by_id(self._person)

   def set_person(self, person: Person) -> _Self:
      self._change('person', person.get_id())
      self._person = person.get_id()
      return self

   def get_subjects(self) -> list[_Entity]:
      from .subject import Subject
      return self._select_many2many(Subject, 'Student_Subject')

   def add_subject(self, subject: _Entity) -> _Self:
      self._add_many2many(subject, 'Student_Subject')
      return self

   def remove_subject(self, subject: _Entity) -> _Self:
      self._remove_many2many(subject, 'Student_Subject')
      return self

   def as_dict(self) -> dict:
      result = dict()
      result['id'] = self.get_id()
      result['person'] = self._person
      return result

   def _get_many2many_relations(self) -> list[str]:
      relations = []
      relations.append('Student_Subject')
      return relations

