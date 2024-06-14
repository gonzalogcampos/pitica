from __future__ import annotations as _annotations
from typing import List as _List
from datetime import datetime as _datetime
import logging as _logging

import pitica as _pitica
from pitica import constants as _constants
from pitica.filter import Filter as _Filter
from pitica.filter import FilterGroup as _FilterGroup
from pitica.filter import FilterOperator as _FilterOperator
from pitica.persistance.persistance import Persistance as _Persistance
from pitica.notifications.notifications import Notifications as _Notifications

_logger = _logging.getLogger(__name__)


class Entity:
    def __init__(self, class_type):
        self.__class_type: type = class_type
        self.__id: int = None
        self.__changes: dict = {}
        self.__relation_changes: dict = {}

    def get_id(self) -> str:
        return self.__id

    def create(self) -> Entity:
        if self.get_id() is not None:
            msg = f"{self.__class_type.__name__} with id {self.get_id()} already exists"
            _logger.error(msg)
            raise Exception(msg)

        classname = self.__class_type.__name__
        _logger.debug(f"Creating new {classname} | {self.as_dict()}")

        self.__id = Entity._get_persistance().insert(
            table=classname, data=self.as_dict())
        self._persist_relations()

        Entity._get_notifications().notify(
            classname, _Notifications.Type.CREATION, self.as_dict())
        self._notify_relations()

        self.__changes = {}
        self.__relation_changes = {}

        return self

    def update(self) -> Entity:
        classname = self.__class_type.__name__

        if self.get_id() is None:
            msg = f"{classname} can't be updated because it doesn't exist"
            _logger.error(msg)
            raise Exception(msg)

        _logger.debug(
            f"Updating {classname} {self.get_id()} | {self.as_dict()}")
        data = {k: v['to'] for k, v in self.__changes.items()}

        changes = self.__changes
        changes[_constants.ID_ATTRIBUTE] = self.get_id()

        Entity._get_persistance().update(table=classname, id=self.get_id(), data=data)
        self._persist_relations()

        Entity._get_notifications().notify(classname, _Notifications.Type.EDITION, changes)
        self._notify_relations()

        self.__changes = {}
        self.__relation_changes = {}

        return self

    def _persist_relations(self):
        self_classname = self.__class_type.__name__
        for relation_table, target_classname in self.__relation_changes:
            changes_data = self.__relation_changes[(
                relation_table, target_classname)]

            for add_id in changes_data["add"]:
                data = {target_classname: add_id,
                        self_classname: self.get_id()}
                Entity._get_persistance().insert(relation_table, data)
                _logger.debug(
                    f"Adding relation {target_classname}:{add_id} {self_classname}:{self.get_id()}")

            for remove_id in changes_data["remove"]:
                filter_group = _FilterGroup()
                filter_group.and_(_Filter(target_classname,
                                          _FilterOperator.EQUALS, remove_id))
                filter_group.and_(_Filter(self.__class_type.__name__,
                                          _FilterOperator.EQUALS, self.get_id()))
                _logger.debug(
                    f"Removing relation {target_classname}:{remove_id} {self_classname}:{self.get_id()}")
                Entity._get_persistance().delete(relation_table, filter_group)

    def _notify_relations(self):
        # Entity._get_notifications().notify(self.__class_type.__name__,
        #                                    _Notifications.Type.EDITION, {})
        pass

    def delete(self) -> Entity:
        classname = self.__class_type.__name__

        if self.get_id() is None:
            msg = f"{classname} can't be updated because it doesn't exist"
            _logger.error(msg)
            raise Exception(msg)

        self._remove_many2many_relations()
        id_filter = _Filter(_constants.ID_ATTRIBUTE,
                            _FilterOperator.EQUALS, self.get_id())

        _logger.debug(f"Removing {classname} {self.get_id()}")

        Entity._get_persistance().delete(table=classname, filters=id_filter)

        Entity._get_notifications().notify(
            classname, _Notifications.Type.DELETION, self.as_dict())

        self.__id = None
        return self

    def as_dict(self) -> dict:
        return {}

    def _select_many2many(self, class_type: type, relation_table: str) -> _List[Entity]:
        items = Entity._get_persistance().select_many2many(table=class_type.__name__,
                                                           relation_table=relation_table,
                                                           target=self.__class_type.__name__,
                                                           target_id=self.get_id()
                                                           )
        return [class_type.from_dict(item) for item in items]

    def _get_many2many_relations(self) -> list[str]:
        return []

    def _remove_many2many_relations(self) -> Entity:
        _logger.debug(
            f"Removing all relations of {self.__class_type.__name__}:{self.get_id()}")

        for relation_table in self._get_many2many_relations():
            id_filter = _Filter(self.__class_type.__name__,
                                _FilterOperator.EQUALS, self.get_id())
            Entity._get_persistance().delete(relation_table, id_filter)

    def _change(self, id, value) -> None:
        from_value = self.__changes.get(id, {}).get("from", self.as_dict()[id])

        if isinstance(value, _datetime):
            value = value.isoformat()
        if isinstance(from_value, _datetime):
            from_value = from_value.isoformat()

        self.__changes[id] = {"from": from_value, "to": value}

    def _add_many2many(self, target: Entity, relation_table: str) -> None:
        self._edit_many2many(target, relation_table, "add")

    def _remove_many2many(self, target: Entity, relation_table: str) -> None:
        self._edit_many2many(target, relation_table, "remove")

    def _edit_many2many(self, target: Entity, relation_table: str, change_type: str) -> None:
        added = "add"
        removed = "remove"

        add_to = change_type
        rem_to = added if change_type == removed else removed

        key = (relation_table, target.__class_type.__name__)

        if key not in self.__relation_changes:
            self.__relation_changes[key] = {
                added: set(), removed: set()}

        if target.get_id() not in self.__relation_changes[key][add_to]:
            self.__relation_changes[key][add_to].add(target.get_id())
        if target.get_id() in self.__relation_changes[key][rem_to]:
            self.__relation_changes[key][rem_to].remove(target.get_id())

    @staticmethod
    def _get_persistance() -> _Persistance:
        return _pitica.get_repository()

    @staticmethod
    def _get_notifications() -> _Notifications:
        return _pitica.get_notifications()

    @classmethod
    def from_dict(this, data: dict) -> Entity:
        instance = this()
        for key, value in data.items():
            if key == _constants.ID_ATTRIBUTE:
                instance.__setattr__(f"_Entity__{key}", value)
            else:
                try:
                    getattr(instance, f"set_{key}")(value)
                except AttributeError:
                    instance.__setattr__(f"_{key}", value)
        instance.__relation_changes = {}
        return instance

    @classmethod
    def find_all(this, filters: _Filter = None) -> _List[Entity]:
        _logger.debug(
            f"Getting all {this.__name__} | Filter {str(filters)}")
        items = Entity._get_persistance().select(
            table=this.__name__,
            filters=filters
        )
        return [this.from_dict(item) for item in items]

    @classmethod
    def find_by_id(this, id: int) -> Entity:
        _logger.debug(f"Getting {this.__name__}:{id}")
        id_filter = _Filter(_constants.ID_ATTRIBUTE,
                            _FilterOperator.EQUALS, id)
        items = Entity._get_persistance().select(
            table=this.__name__,
            filters=id_filter
        )
        if len(items) != 1:
            return None
        return this.from_dict(items[0])
