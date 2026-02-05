from __future__ import annotations

import types
from dataclasses import MISSING, fields, is_dataclass
from datetime import datetime
from typing import Any, TypeVar, Union, get_args, get_origin, get_type_hints

from metaspn_schemas.utils.time import datetime_to_str, str_to_datetime

T = TypeVar("T")


class Serializable:
    def to_dict(self, *, privacy_mode: bool = False) -> dict[str, Any]:
        return dataclass_to_dict(self, privacy_mode=privacy_mode)

    @classmethod
    def from_dict(cls: type[T], data: dict[str, Any]) -> T:
        return dataclass_from_dict(cls, data)


def dataclass_to_dict(obj: Any, *, privacy_mode: bool = False) -> dict[str, Any]:
    if not is_dataclass(obj):
        raise TypeError("dataclass_to_dict expects a dataclass instance")

    output: dict[str, Any] = {}
    for f in fields(obj):
        if privacy_mode and f.metadata.get("omit_in_privacy_mode"):
            continue
        value = getattr(obj, f.name)
        output[f.name] = _to_primitive(value, privacy_mode=privacy_mode)
    return output


def _to_primitive(value: Any, *, privacy_mode: bool) -> Any:
    if is_dataclass(value):
        return dataclass_to_dict(value, privacy_mode=privacy_mode)
    if isinstance(value, datetime):
        return datetime_to_str(value)
    if isinstance(value, tuple):
        return [_to_primitive(v, privacy_mode=privacy_mode) for v in value]
    if isinstance(value, list):
        return [_to_primitive(v, privacy_mode=privacy_mode) for v in value]
    if isinstance(value, dict):
        return {k: _to_primitive(v, privacy_mode=privacy_mode) for k, v in sorted(value.items())}
    return value


def dataclass_from_dict(cls: type[T], data: dict[str, Any]) -> T:
    if not is_dataclass(cls):
        raise TypeError("dataclass_from_dict expects a dataclass type")

    hints = get_type_hints(cls)
    kwargs: dict[str, Any] = {}

    for f in fields(cls):
        hint = hints.get(f.name, Any)
        if f.name in data:
            kwargs[f.name] = _coerce_value(hint, data[f.name])
            continue

        if f.default is not MISSING:
            kwargs[f.name] = f.default
            continue

        if f.default_factory is not MISSING:  # type: ignore[attr-defined]
            kwargs[f.name] = f.default_factory()  # type: ignore[misc]
            continue

        raise ValueError(f"Missing required field: {f.name}")

    return cls(**kwargs)


def _coerce_value(hint: Any, value: Any) -> Any:
    if value is None:
        return None

    origin = get_origin(hint)
    args = get_args(hint)

    if hint is Any:
        return value

    if hint is datetime:
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            return str_to_datetime(value)
        raise TypeError(f"Cannot parse datetime from {type(value)!r}")

    if origin in (Union, types.UnionType):
        last_error: Exception | None = None
        for option in args:
            if option is type(None):
                continue
            try:
                return _coerce_value(option, value)
            except Exception as err:  # noqa: BLE001
                last_error = err
        if last_error is not None:
            raise last_error
        return value

    if origin is tuple:
        item_type = args[0] if args else Any
        return tuple(_coerce_value(item_type, item) for item in value)

    if origin is list:
        item_type = args[0] if args else Any
        return [_coerce_value(item_type, item) for item in value]

    if origin is dict:
        key_type = args[0] if len(args) > 0 else Any
        value_type = args[1] if len(args) > 1 else Any
        return {
            _coerce_value(key_type, k): _coerce_value(value_type, v)
            for k, v in value.items()
        }

    if is_dataclass(hint):
        if isinstance(value, hint):
            return value
        if isinstance(value, dict):
            return dataclass_from_dict(hint, value)

    if hint in (str, int, float, bool):
        return hint(value)

    return value
