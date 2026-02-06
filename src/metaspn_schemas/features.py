from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from metaspn_schemas.core import DEFAULT_SCHEMA_VERSION
from metaspn_schemas.utils.serde import Serializable
from metaspn_schemas.utils.time import ensure_utc


@dataclass(frozen=True)
class ProfileEnriched(Serializable):
    entity_id: str
    enriched_at: datetime
    summary: str
    topics: tuple[str, ...] = field(default_factory=tuple)
    schema_version: str = DEFAULT_SCHEMA_VERSION

    def __post_init__(self) -> None:
        object.__setattr__(self, "enriched_at", ensure_utc(self.enriched_at))
        object.__setattr__(self, "topics", tuple(sorted(self.topics)))


@dataclass(frozen=True)
class ScoresComputed(Serializable):
    entity_id: str
    computed_at: datetime
    scores: dict[str, float]
    scorer: str
    schema_version: str = DEFAULT_SCHEMA_VERSION

    def __post_init__(self) -> None:
        object.__setattr__(self, "computed_at", ensure_utc(self.computed_at))


@dataclass(frozen=True)
class PlaybookRouted(Serializable):
    task_id: str
    routed_at: datetime
    playbook: str
    rationale: str | None = None
    schema_version: str = DEFAULT_SCHEMA_VERSION

    def __post_init__(self) -> None:
        object.__setattr__(self, "routed_at", ensure_utc(self.routed_at))


@dataclass(frozen=True)
class GameClassified(Serializable):
    entity_id: str
    classified_at: datetime
    label: str
    confidence: float
    schema_version: str = DEFAULT_SCHEMA_VERSION

    def __post_init__(self) -> None:
        object.__setattr__(self, "classified_at", ensure_utc(self.classified_at))


@dataclass(frozen=True)
class M1ProfileEnrichment(Serializable):
    enrichment_id: str
    entity_id: str
    enriched_at: datetime
    role: str
    organization: str
    topics: tuple[str, ...]
    evidence_summary: str
    schema_version: str = DEFAULT_SCHEMA_VERSION
    metadata: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "enriched_at", ensure_utc(self.enriched_at))
        object.__setattr__(self, "topics", tuple(sorted(self.topics)))


@dataclass(frozen=True)
class M1ScoreCard(Serializable):
    score_id: str
    entity_id: str
    computed_at: datetime
    fit: float
    quality: float
    reply_likelihood: float
    scorer: str
    schema_version: str = DEFAULT_SCHEMA_VERSION
    scorer_metadata: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "computed_at", ensure_utc(self.computed_at))


@dataclass(frozen=True)
class M1RoutingRecommendation(Serializable):
    recommendation_id: str
    entity_id: str
    recommended_at: datetime
    playbook: str
    rationale: str
    priority: int
    suggested_action: str
    schema_version: str = DEFAULT_SCHEMA_VERSION
    metadata: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "recommended_at", ensure_utc(self.recommended_at))
