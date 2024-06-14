from typing import List as _List
from enum import Enum as _Enum


class FilterOperator(_Enum):
    EQUALS = 1
    NOT_EQUALS = 2
    IS = 3
    IS_NOT = 4
    LESS = 5
    LESS_OR_EQUAL = 6
    GREATER = 7
    GREATER_OR_EQUAL = 8
    AND = 9
    OR = 10


_OPERATOR2HUMAN = {
    FilterOperator.EQUALS: "==",
    FilterOperator.NOT_EQUALS: "!=",
    FilterOperator.IS: "is",
    FilterOperator.IS_NOT: "is not",
    FilterOperator.LESS: "<",
    FilterOperator.LESS_OR_EQUAL: "<=",
    FilterOperator.GREATER: ">",
    FilterOperator.GREATER_OR_EQUAL: ">=",
    FilterOperator.AND: "and",
    FilterOperator.OR: "or",
}


class Filter:
    def __init__(self, a: object, operator: FilterOperator, b: object):
        self.a = a
        self.operator = operator
        self.b = b

    def get_representation(self) -> tuple:
        return [(self.a, self.operator, self.b)]

    def __str__(self) -> str:
        return f"{self.a} {_OPERATOR2HUMAN[self.operator]} {self.b}"


class FilterGroup(Filter):

    class Item:
        def __init__(self, append_type, filter):
            self.append_type = append_type
            self.filter: Filter = filter

    def __init__(self):
        self._items: _List[FilterGroup.Item] = []

    def and_(self, filter: Filter) -> None:
        self._items.append(FilterGroup.Item(FilterOperator.AND, filter))

    def or_(self, filter: Filter) -> None:
        self._items.append(FilterGroup.Item(FilterOperator.OR, filter))

    def get_representation(self) -> list:
        representation = []
        for item in self._items:
            if representation:
                representation.append(item.append_type)
            representation.append(item.filter.get_representation())
        return representation

    def __str__(self) -> str:
        result = ""

        if len(self._items) == 1:
            return str(self._items[0])

        for item in self._items:
            if result:
                result = f"{result} {str(item.append_type)} ({str(item.filter)})"
            else:
                result = f"({str(item.filter)})"
        return result
