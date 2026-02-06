from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from metaspn_schemas.core import DEFAULT_SCHEMA_VERSION
from metaspn_schemas.utils.serde import Serializable
from metaspn_schemas.utils.time import ensure_utc


@dataclass(frozen=True)
class Recommendation(Serializable):
    recommendation_id: str
    entity_id: str
    playbook: str
    score: float
    rationale: str
    priority: int
    created_at: datetime
    schema_version: str = DEFAULT_SCHEMA_VERSION
    metadata: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "created_at", ensure_utc(self.created_at))


@dataclass(frozen=True)
class DailyDigestEntry(Serializable):
    digest_entry_id: str
    entity_id: str
    rank: int
    action_item: str
    created_at: datetime
    schema_version: str = DEFAULT_SCHEMA_VERSION
    metadata: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "created_at", ensure_utc(self.created_at))


@dataclass(frozen=True)
class DraftMessage(Serializable):
    draft_id: str
    entity_id: str
    channel: str
    body: str
    tone: str
    created_at: datetime
    schema_version: str = DEFAULT_SCHEMA_VERSION
    subject: str | None = None
    constraints: tuple[str, ...] = field(default_factory=tuple)
    metadata: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "created_at", ensure_utc(self.created_at))
        object.__setattr__(self, "constraints", tuple(sorted(self.constraints)))


@dataclass(frozen=True)
class ApprovalOverride(Serializable):
    approval_id: str
    draft_id: str
    status: str
    reason: str
    reviewed_at: datetime
    schema_version: str = DEFAULT_SCHEMA_VERSION
    edited_subject: str | None = None
    edited_body: str | None = None
    reviewer: str | None = None
    metadata: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "reviewed_at", ensure_utc(self.reviewed_at))
