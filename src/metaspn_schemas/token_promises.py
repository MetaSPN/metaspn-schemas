from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from metaspn_schemas.core import DEFAULT_SCHEMA_VERSION
from metaspn_schemas.utils.serde import Serializable
from metaspn_schemas.utils.time import ensure_utc


@dataclass(frozen=True)
class TokenSignalSeen(Serializable):
    token_signal_id: str
    token_id: str
    creator_id: str
    signal_type: str
    seen_at: datetime
    schema_version: str = DEFAULT_SCHEMA_VERSION
    metadata: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "seen_at", ensure_utc(self.seen_at))


@dataclass(frozen=True)
class PromiseRegistered(Serializable):
    promise_id: str
    token_id: str
    creator_id: str
    registered_at: datetime
    promise_text: str
    schema_version: str = DEFAULT_SCHEMA_VERSION
    source: str | None = None
    metadata: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "registered_at", ensure_utc(self.registered_at))


@dataclass(frozen=True)
class PromiseEvaluated(Serializable):
    evaluation_id: str
    promise_id: str
    token_id: str
    evaluated_at: datetime
    status: str
    confidence: float
    schema_version: str = DEFAULT_SCHEMA_VERSION
    rationale: str | None = None
    metadata: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "evaluated_at", ensure_utc(self.evaluated_at))


@dataclass(frozen=True)
class TokenHealthScoreCard(Serializable):
    scorecard_id: str
    token_id: str
    computed_at: datetime
    health_score: float
    risk_score: float
    momentum_score: float
    schema_version: str = DEFAULT_SCHEMA_VERSION
    scorer: str | None = None
    metrics: dict[str, float] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "computed_at", ensure_utc(self.computed_at))


@dataclass(frozen=True)
class TokenOutcomeObserved(Serializable):
    outcome_observed_id: str
    token_id: str
    observed_at: datetime
    outcome_type: str
    success: bool
    schema_version: str = DEFAULT_SCHEMA_VERSION
    value: float | None = None
    metadata: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "observed_at", ensure_utc(self.observed_at))


@dataclass(frozen=True)
class TokenOutcomeWindow(Serializable):
    token_outcome_window_id: str
    token_id: str
    window_start: datetime
    window_end: datetime
    evaluated_at: datetime
    success_rate: float
    schema_version: str = DEFAULT_SCHEMA_VERSION
    outcomes: tuple[str, ...] = field(default_factory=tuple)
    metrics: dict[str, float] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "window_start", ensure_utc(self.window_start))
        object.__setattr__(self, "window_end", ensure_utc(self.window_end))
        object.__setattr__(self, "evaluated_at", ensure_utc(self.evaluated_at))
        object.__setattr__(self, "outcomes", tuple(sorted(self.outcomes)))


@dataclass(frozen=True)
class PromisePredictiveAccuracy(Serializable):
    predictive_accuracy_id: str
    promise_id: str
    measured_at: datetime
    accuracy: float
    sample_size: int
    schema_version: str = DEFAULT_SCHEMA_VERSION
    calibration_error: float | None = None
    metadata: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "measured_at", ensure_utc(self.measured_at))


@dataclass(frozen=True)
class CreatorBehaviorCorrelation(Serializable):
    creator_correlation_id: str
    creator_id: str
    computed_at: datetime
    behavior_signal: str
    outcome_signal: str
    correlation: float
    schema_version: str = DEFAULT_SCHEMA_VERSION
    p_value: float | None = None
    metadata: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "computed_at", ensure_utc(self.computed_at))
