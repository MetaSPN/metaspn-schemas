from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from metaspn_schemas.core import DEFAULT_SCHEMA_VERSION
from metaspn_schemas.utils.serde import Serializable


@dataclass(frozen=True)
class ProfileEnriched(Serializable):
    entity_id: str
    enriched_at: datetime
    summary: str
    topics: tuple[str, ...] = field(default_factory=tuple)
    schema_version: str = DEFAULT_SCHEMA_VERSION

    def __post_init__(self) -> None:
        object.__setattr__(self, "topics", tuple(sorted(self.topics)))


@dataclass(frozen=True)
class ScoresComputed(Serializable):
    entity_id: str
    computed_at: datetime
    scores: dict[str, float]
    scorer: str
    schema_version: str = DEFAULT_SCHEMA_VERSION


@dataclass(frozen=True)
class PlaybookRouted(Serializable):
    task_id: str
    routed_at: datetime
    playbook: str
    rationale: str | None = None
    schema_version: str = DEFAULT_SCHEMA_VERSION


@dataclass(frozen=True)
class GameClassified(Serializable):
    entity_id: str
    classified_at: datetime
    label: str
    confidence: float
    schema_version: str = DEFAULT_SCHEMA_VERSION
