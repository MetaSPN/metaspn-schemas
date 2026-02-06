from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from metaspn_schemas.core import DEFAULT_SCHEMA_VERSION
from metaspn_schemas.utils.serde import Serializable
from metaspn_schemas.utils.time import ensure_utc


@dataclass(frozen=True)
class LearningOutcomeWindow(Serializable):
    window_id: str
    entity_id: str
    attempted_at: datetime
    window_start: datetime
    window_end: datetime
    outcome: str
    success: bool
    schema_version: str = DEFAULT_SCHEMA_VERSION
    metrics: dict[str, float] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "attempted_at", ensure_utc(self.attempted_at))
        object.__setattr__(self, "window_start", ensure_utc(self.window_start))
        object.__setattr__(self, "window_end", ensure_utc(self.window_end))


@dataclass(frozen=True)
class FailureLabel(Serializable):
    label_id: str
    entity_id: str
    category: str
    code: str
    evidence: str
    labeled_at: datetime
    schema_version: str = DEFAULT_SCHEMA_VERSION
    metadata: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "labeled_at", ensure_utc(self.labeled_at))


@dataclass(frozen=True)
class GateCalibrationRecommendation(Serializable):
    recommendation_id: str
    gate_name: str
    created_at: datetime
    threshold_delta: float
    cooldown_seconds_delta: int
    confidence: float
    rationale: str
    schema_version: str = DEFAULT_SCHEMA_VERSION
    based_on_windows: tuple[str, ...] = field(default_factory=tuple)
    metadata: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "created_at", ensure_utc(self.created_at))
        object.__setattr__(self, "based_on_windows", tuple(sorted(self.based_on_windows)))


@dataclass(frozen=True)
class PolicyOverrideReview(Serializable):
    review_id: str
    recommendation_id: str
    decision: str
    reviewed_at: datetime
    reviewer: str
    reason: str
    schema_version: str = DEFAULT_SCHEMA_VERSION
    applied_threshold_delta: float | None = None
    applied_cooldown_seconds_delta: int | None = None
    metadata: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "reviewed_at", ensure_utc(self.reviewed_at))
