# Auto generated from Model SQL (c)
# Copyright Gonzalo G. Campos 2024

from typing import Self as _Self
from pitica.entity import Entity as _Entity
from pitica.filter import Filter as _Filter
from pitica.filter import FilterOperator as _FilterOperator
from .teacher import Teacher


class Subject(_Entity):
   def __init__(self):
      super().__init__(Subject)
      self._name = None
      self._teacher = None

   def get_name(self) -> str:
      return self._name

   def set_name(self, value: str) -> _Self:
      self._change('name', value)
      self._name = value
      return self

   def get_teacher(self) -> Teacher:
      return Teacher.find_by_id(self._teacher)

   def set_teacher(self, teacher: Teacher) -> _Self:
      self._change('teacher', teacher.get_id())
      self._teacher = teacher.get_id()
      return self

   def get_students(self) -> list[_Entity]:
      from .student import Student
      return self._select_many2many(Student, 'Student_Subject')

   def add_student(self, student: _Entity) -> _Self:
      self._add_many2many(student, 'Student_Subject')
      return self

   def remove_student(self, student: _Entity) -> _Self:
      self._remove_many2many(student, 'Student_Subject')
      return self

   def as_dict(self) -> dict:
      result = dict()
      result['id'] = self.get_id()
      result['name'] = self._name
      result['teacher'] = self._teacher
      return result

   def _get_many2many_relations(self) -> list[str]:
      relations = []
      relations.append('Student_Subject')
      return relations

   @staticmethod
   def find_by_name(name: str, filter_operator: _FilterOperator = _FilterOperator.EQUALS) -> _Self:
      filters = _Filter('name', filter_operator, name)
      all = Subject.find_all(filters=filters)
      if all:
         return all[0]
      return None

