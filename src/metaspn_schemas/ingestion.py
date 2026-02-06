from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from metaspn_schemas.core import DEFAULT_SCHEMA_VERSION, EntityRef
from metaspn_schemas.utils.serde import Serializable
from metaspn_schemas.utils.time import ensure_utc


@dataclass(frozen=True)
class ResolverHandoff(Serializable):
    handoff_id: str
    entity_ref: EntityRef
    provenance_source: str
    provenance_step: str
    attached_at: datetime
    schema_version: str = DEFAULT_SCHEMA_VERSION
    metadata: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "attached_at", ensure_utc(self.attached_at))


@dataclass(frozen=True)
class RawSocialPostSeenEvent(Serializable):
    event_id: str
    source: str
    seen_at: datetime
    raw: dict[str, Any]
    schema_version: str = DEFAULT_SCHEMA_VERSION
    resolver_handoff: ResolverHandoff | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "seen_at", ensure_utc(self.seen_at))


@dataclass(frozen=True)
class NormalizedSocialPostSeenEvent(Serializable):
    event_id: str
    source: str
    platform: str
    post_id: str
    author_handle: str
    content: str
    seen_at: datetime
    schema_version: str = DEFAULT_SCHEMA_VERSION
    post_url: str | None = None
    topics: tuple[str, ...] = field(default_factory=tuple)
    resolver_handoff: ResolverHandoff | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "seen_at", ensure_utc(self.seen_at))
        object.__setattr__(self, "topics", tuple(sorted(self.topics)))


@dataclass(frozen=True)
class IngestionParseErrorEvent(Serializable):
    error_id: str
    source: str
    occurred_at: datetime
    error_type: str
    message: str
    schema_version: str = DEFAULT_SCHEMA_VERSION
    raw_payload: dict[str, Any] = field(default_factory=dict)
    resolver_handoff: ResolverHandoff | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "occurred_at", ensure_utc(self.occurred_at))
