import ctypes as _ctypes
from datetime import datetime as _datetime

NAME = "pitica"

SCHEMA_FILENAME = f"{NAME}.yml"
DEFAULT_DB_NAME = f"{NAME}"
DEFAULT_DB_HOST = "localhost"
DEFAULT_DB_PORT = 3360

DEFAULT_NOTIFICATION_HOST = "localhost"
DEFAULT_NOTIFICATION_PORT = 6379

ID_ATTRIBUTE = "id"

FORBIDDEN_ARGS = [
    ID_ATTRIBUTE
]

K_TYPE = "type"
K_ATTRIBUTE_TYPE = "attribute_type"
K_RELATION_TYPE = "relation_type"
K_RELATION_TARGET = "relation_target"
K_UNIQUE = "unique"
K_MANDATORY = "mandatory"

ATTRIBUTE = "attribute"
RELATION = "relation"

TYPES_CONVERSION = {
    "float": float,
    "int": int,
    "integer": int,
    "uint": _ctypes.c_uint,
    "uinteger": _ctypes.c_uint,
    "unsignedint": _ctypes.c_uint,
    "unsignedinteger": _ctypes.c_uint,
    "bool": bool,
    "boolean": bool,
    "str": str,
    "string": str,
    "datetime": _datetime,
    ID_ATTRIBUTE: ID_ATTRIBUTE
}

ONE2ONE = "one2one"
ONE2MANY = "one2many"
MANY2MANY = "many2many"
