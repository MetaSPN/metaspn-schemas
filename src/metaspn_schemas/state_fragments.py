from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from metaspn_schemas.core import DEFAULT_SCHEMA_VERSION
from metaspn_schemas.utils.serde import Serializable


@dataclass(frozen=True)
class Identity(Serializable):
    entity_id: str
    canonical_name: str | None = None
    aliases: tuple[str, ...] = field(default_factory=tuple)
    schema_version: str = DEFAULT_SCHEMA_VERSION


@dataclass(frozen=True)
class Evidence(Serializable):
    evidence_id: str
    entity_id: str
    source: str
    collected_at: datetime
    attributes: dict[str, str] = field(default_factory=dict)
    schema_version: str = DEFAULT_SCHEMA_VERSION


@dataclass(frozen=True)
class Scores(Serializable):
    entity_id: str
    values: dict[str, float]
    updated_at: datetime
    schema_version: str = DEFAULT_SCHEMA_VERSION


@dataclass(frozen=True)
class Cooldowns(Serializable):
    entity_id: str
    channel: str
    until: datetime
    reason: str | None = None
    schema_version: str = DEFAULT_SCHEMA_VERSION


@dataclass(frozen=True)
class Attempts(Serializable):
    entity_id: str
    count: int
    last_attempt_at: datetime | None = None
    schema_version: str = DEFAULT_SCHEMA_VERSION
