from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Mapping

from metaspn_schemas.core import DEFAULT_SCHEMA_VERSION
from metaspn_schemas.utils.serde import Serializable
from metaspn_schemas.utils.time import ensure_utc


@dataclass(frozen=True)
class StateTransitionRule(Serializable):
    from_state: str
    to_state: str
    event: str
    guard: str | None = None
    schema_version: str = DEFAULT_SCHEMA_VERSION


@dataclass(frozen=True)
class StateMachineConfig(Serializable):
    config_id: str
    machine_type: str
    initial_state: str
    states: tuple[str, ...]
    transitions: tuple[StateTransitionRule, ...]
    schema_version: str = DEFAULT_SCHEMA_VERSION
    terminal_states: tuple[str, ...] = field(default_factory=tuple)
    metadata: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "states", tuple(sorted(self.states)))
        object.__setattr__(self, "terminal_states", tuple(sorted(self.terminal_states)))
        sorted_transitions = tuple(
            sorted(
                self.transitions,
                key=lambda t: (t.from_state, t.event, t.to_state, t.guard or ""),
            )
        )
        object.__setattr__(self, "transitions", sorted_transitions)


@dataclass(frozen=True)
class GateTransitionAttempt(Serializable):
    attempt_id: str
    gate_name: str
    entity_id: str
    from_state: str
    to_state: str
    attempted_at: datetime
    allowed: bool
    schema_version: str = DEFAULT_SCHEMA_VERSION
    reason_code: str | None = None
    caused_by: tuple[str, ...] = field(default_factory=tuple)
    context: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "attempted_at", ensure_utc(self.attempted_at))


@dataclass(frozen=True)
class OutcomeWindowEvaluation(Serializable):
    evaluation_id: str
    entity_id: str
    window_start: datetime
    window_end: datetime
    evaluated_at: datetime
    outcome_type: str
    success: bool
    schema_version: str = DEFAULT_SCHEMA_VERSION
    metrics: dict[str, float] = field(default_factory=dict)
    caused_by_attempt_id: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "window_start", ensure_utc(self.window_start))
        object.__setattr__(self, "window_end", ensure_utc(self.window_end))
        object.__setattr__(self, "evaluated_at", ensure_utc(self.evaluated_at))


@dataclass(frozen=True)
class CalibrationRecord(Serializable):
    calibration_id: str
    model_name: str
    calibrated_at: datetime
    sample_size: int
    threshold: float
    schema_version: str = DEFAULT_SCHEMA_VERSION
    precision: float | None = None
    recall: float | None = None
    notes: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "calibrated_at", ensure_utc(self.calibrated_at))


@dataclass(frozen=True)
class FailureTaxonomyRecord(Serializable):
    failure_id: str
    category: str
    code: str
    observed_at: datetime
    severity: str
    schema_version: str = DEFAULT_SCHEMA_VERSION
    description: str | None = None
    tags: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        object.__setattr__(self, "observed_at", ensure_utc(self.observed_at))
        object.__setattr__(self, "tags", tuple(sorted(self.tags)))


def parse_state_machine_config(data: Mapping[str, Any]) -> StateMachineConfig:
    normalized = _normalize_state_machine_payload(data)
    return StateMachineConfig.from_dict(normalized)


def validate_state_machine_config(
    config_or_payload: StateMachineConfig | Mapping[str, Any],
) -> tuple[bool, tuple[str, ...]]:
    try:
        config = (
            config_or_payload
            if isinstance(config_or_payload, StateMachineConfig)
            else parse_state_machine_config(config_or_payload)
        )
    except Exception as err:  # noqa: BLE001
        return (False, (f"parse_error: {err}",))

    errors: list[str] = []

    if not config.states:
        errors.append("states must contain at least one value")

    state_set = set(config.states)

    if config.initial_state not in state_set:
        errors.append("initial_state must exist in states")

    unknown_terminal = sorted(set(config.terminal_states) - state_set)
    if unknown_terminal:
        errors.append(f"terminal_states must be a subset of states: {','.join(unknown_terminal)}")

    if not config.transitions:
        errors.append("transitions must contain at least one rule")

    seen_edges: set[tuple[str, str, str]] = set()
    for rule in config.transitions:
        if rule.from_state not in state_set:
            errors.append(f"transition from_state not in states: {rule.from_state}")
        if rule.to_state not in state_set:
            errors.append(f"transition to_state not in states: {rule.to_state}")

        edge_key = (rule.from_state, rule.event, rule.to_state)
        if edge_key in seen_edges:
            errors.append(
                f"duplicate transition rule: {rule.from_state}|{rule.event}|{rule.to_state}"
            )
        seen_edges.add(edge_key)

    deduped = tuple(dict.fromkeys(errors))
    return (not deduped, deduped)


def _normalize_state_machine_payload(data: Mapping[str, Any]) -> dict[str, Any]:
    normalized = dict(data)

    if "machine_id" in normalized and "config_id" not in normalized:
        normalized["config_id"] = normalized["machine_id"]

    if "machine_name" in normalized and "machine_type" not in normalized:
        normalized["machine_type"] = normalized["machine_name"]

    if "start_state" in normalized and "initial_state" not in normalized:
        normalized["initial_state"] = normalized["start_state"]

    if "state_nodes" in normalized and "states" not in normalized:
        normalized["states"] = normalized["state_nodes"]

    if "end_states" in normalized and "terminal_states" not in normalized:
        normalized["terminal_states"] = normalized["end_states"]

    transitions = normalized.get("transitions", [])
    normalized_transitions: list[dict[str, Any]] = []
    for transition in transitions:
        if isinstance(transition, StateTransitionRule):
            normalized_transitions.append(transition.to_dict())
            continue

        row = dict(transition)
        from_state = row.get("from_state", row.get("from"))
        to_state = row.get("to_state", row.get("to"))
        event = row.get("event", row.get("event_name"))
        normalized_transitions.append(
            {
                "from_state": from_state,
                "to_state": to_state,
                "event": event,
                "guard": row.get("guard"),
                "schema_version": row.get("schema_version", DEFAULT_SCHEMA_VERSION),
            }
        )
    normalized["transitions"] = normalized_transitions

    if "schema_version" not in normalized:
        normalized["schema_version"] = DEFAULT_SCHEMA_VERSION

    return normalized
