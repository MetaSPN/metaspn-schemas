from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from metaspn_schemas.core import DEFAULT_SCHEMA_VERSION, EntityRef
from metaspn_schemas.utils.serde import Serializable


@dataclass(frozen=True)
class Task(Serializable):
    task_id: str
    task_type: str
    created_at: datetime
    priority: int
    entity_ref: EntityRef
    inputs: dict[str, Any] = field(default_factory=dict)
    context: dict[str, Any] = field(default_factory=dict)
    schema_version: str = DEFAULT_SCHEMA_VERSION


@dataclass(frozen=True)
class Result(Serializable):
    result_id: str
    task_id: str
    status: str
    completed_at: datetime
    outputs: dict[str, Any] = field(default_factory=dict)
    errors: tuple[str, ...] = field(default_factory=tuple)
    schema_version: str = DEFAULT_SCHEMA_VERSION
