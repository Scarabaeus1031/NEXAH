"""Shared validation and serialization support for orientation contracts."""

from __future__ import annotations

from dataclasses import fields, is_dataclass
from datetime import datetime
from enum import Enum
from types import UnionType
from typing import Any, Mapping, TypeVar, Union, cast, get_args, get_origin, get_type_hints


ContractT = TypeVar("ContractT", bound="ContractModel")


def require_text(value: str, field_name: str) -> None:
    """Reject empty identifiers and descriptions at contract boundaries."""

    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")


def require_aware_datetime(value: datetime, field_name: str) -> None:
    """Require an unambiguous timestamp with timezone information."""

    if not isinstance(value, datetime) or value.tzinfo is None:
        raise ValueError(f"{field_name} must be a timezone-aware datetime")


def _encode(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, datetime):
        return value.isoformat()
    if is_dataclass(value):
        return {
            field.name: _encode(getattr(value, field.name))
            for field in fields(value)
        }
    if isinstance(value, tuple):
        return [_encode(item) for item in value]
    if isinstance(value, list):
        return [_encode(item) for item in value]
    if isinstance(value, Mapping):
        return {str(key): _encode(item) for key, item in value.items()}
    return value


def _decode(annotation: Any, value: Any) -> Any:
    if value is None:
        return None

    if annotation is Any:
        return value

    origin = get_origin(annotation)
    arguments = get_args(annotation)

    if origin in (Union, UnionType):
        candidates = [candidate for candidate in arguments if candidate is not type(None)]
        if not candidates:
            return None
        last_error: Exception | None = None
        for candidate in candidates:
            try:
                return _decode(candidate, value)
            except (TypeError, ValueError) as error:
                last_error = error
        if last_error is not None:
            raise last_error

    if origin in (tuple, list):
        item_type = arguments[0] if arguments else Any
        decoded = [_decode(item_type, item) for item in value]
        return tuple(decoded) if origin is tuple else decoded

    if origin in (dict, Mapping):
        key_type, value_type = arguments if arguments else (Any, Any)
        return {
            _decode(key_type, key): _decode(value_type, item)
            for key, item in value.items()
        }

    if annotation is datetime:
        return datetime.fromisoformat(value)

    if isinstance(annotation, type) and issubclass(annotation, Enum):
        return annotation(value)

    if isinstance(annotation, type) and issubclass(annotation, ContractModel):
        return annotation.from_dict(value)

    return value


class ContractModel:
    """Mixin providing strict, JSON-compatible dictionary round-trips."""

    def to_dict(self) -> dict[str, Any]:
        return cast(dict[str, Any], _encode(self))

    @classmethod
    def from_dict(cls: type[ContractT], data: Mapping[str, Any]) -> ContractT:
        if not isinstance(data, Mapping):
            raise ValueError(f"{cls.__name__} input must be a mapping")

        model_fields = {field.name for field in fields(cast(Any, cls))}
        unknown = set(data) - model_fields
        if unknown:
            names = ", ".join(sorted(unknown))
            raise ValueError(f"Unknown {cls.__name__} fields: {names}")

        hints = get_type_hints(cls)
        values = {
            name: _decode(hints.get(name, Any), value)
            for name, value in data.items()
        }
        try:
            return cls(**values)
        except TypeError as error:
            raise ValueError(f"Invalid {cls.__name__}: {error}") from error
