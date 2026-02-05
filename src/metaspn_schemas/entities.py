from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from metaspn_schemas.core import DEFAULT_SCHEMA_VERSION
from metaspn_schemas.utils.serde import Serializable


@dataclass(frozen=True)
class EntityResolved(Serializable):
    entity_id: str
    resolver: str
    resolved_at: datetime
    confidence: float
    schema_version: str = DEFAULT_SCHEMA_VERSION


@dataclass(frozen=True)
class EntityMerged(Serializable):
    entity_id: str
    merged_from: tuple[str, ...]
    merged_at: datetime
    reason: str | None = None
    schema_version: str = DEFAULT_SCHEMA_VERSION


@dataclass(frozen=True)
class EntityAliasAdded(Serializable):
    entity_id: str
    alias: str
    alias_type: str
    added_at: datetime
    schema_version: str = DEFAULT_SCHEMA_VERSION
