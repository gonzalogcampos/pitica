# Auto generated from Model SQL (c)
# Copyright Gonzalo G. Campos 2024

from typing import Self as _Self
from pitica.entity import Entity as _Entity
from pitica.filter import Filter as _Filter
from pitica.filter import FilterOperator as _FilterOperator


class Person(_Entity):
   def __init__(self):
      super().__init__(Person)
      self._dni = None
      self._name = None
      self._age = None

   def get_dni(self) -> str:
      return self._dni

   def set_dni(self, value: str) -> _Self:
      self._change('dni', value)
      self._dni = value
      return self

   def get_name(self) -> str:
      return self._name

   def set_name(self, value: str) -> _Self:
      self._change('name', value)
      self._name = value
      return self

   def get_age(self) -> int:
      return self._age

   def set_age(self, value: int) -> _Self:
      self._change('age', value)
      self._age = value
      return self

   def get_teacher_person(self) -> _Entity:
      from .teacher import Teacher
      from pitica.filter import FilterOperator
      filters = [['person', FilterOperator.EQUALS, self.get_id()]]
      result = Teacher.find_all(filters=filters)
      return result[0] if result else None

   def get_student_person(self) -> _Entity:
      from .student import Student
      from pitica.filter import FilterOperator
      filters = [['person', FilterOperator.EQUALS, self.get_id()]]
      result = Student.find_all(filters=filters)
      return result[0] if result else None

   def as_dict(self) -> dict:
      result = dict()
      result['id'] = self.get_id()
      result['dni'] = self._dni
      result['name'] = self._name
      result['age'] = self._age
      return result

   def _get_many2many_relations(self) -> list[str]:
      relations = []
      return relations

   @staticmethod
   def find_by_dni(dni: str, filter_operator: _FilterOperator = _FilterOperator.EQUALS) -> _Self:
      filters = _Filter('dni', filter_operator, dni)
      all = Person.find_all(filters=filters)
      if all:
         return all[0]
      return None

   @staticmethod
   def find_by_name(name: str, filter_operator: _FilterOperator = _FilterOperator.EQUALS) -> _Self:
      filters = _Filter('name', filter_operator, name)
      all = Person.find_all(filters=filters)
      return all

   @staticmethod
   def find_by_age(age: int, filter_operator: _FilterOperator = _FilterOperator.EQUALS) -> _Self:
      filters = _Filter('age', filter_operator, age)
      all = Person.find_all(filters=filters)
      return all

