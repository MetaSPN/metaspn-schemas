from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from metaspn_schemas.utils.serde import Serializable
from metaspn_schemas.utils.time import ensure_utc

DEFAULT_SCHEMA_VERSION = "0.9"


@dataclass(frozen=True)
class SchemaVersion(Serializable):
    package: str = "metaspn-schemas"
    version: str = DEFAULT_SCHEMA_VERSION


@dataclass(frozen=True)
class EntityRef(Serializable):
    ref_type: str
    value: str
    platform: str | None = None
    label: str | None = None
    schema_version: str = DEFAULT_SCHEMA_VERSION


@dataclass(frozen=True)
class TraceContext(Serializable):
    trace_id: str
    caused_by: tuple[str, ...] = field(default_factory=tuple)
    provenance: str | None = None
    redactions: tuple[str, ...] = field(default_factory=tuple)
    metadata: dict[str, str] = field(default_factory=dict)
    privacy_mode: bool = False
    schema_version: str = DEFAULT_SCHEMA_VERSION


@dataclass(frozen=True)
class SignalEnvelope(Serializable):
    signal_id: str
    timestamp: datetime
    source: str
    payload_type: str
    payload: Any
    schema_version: str = DEFAULT_SCHEMA_VERSION
    entity_refs: tuple[EntityRef, ...] = field(default_factory=tuple)
    trace: TraceContext | None = None
    raw: dict[str, Any] | None = field(default=None, metadata={"omit_in_privacy_mode": True})

    def __post_init__(self) -> None:
        object.__setattr__(self, "timestamp", ensure_utc(self.timestamp))


@dataclass(frozen=True)
class EmissionEnvelope(Serializable):
    emission_id: str
    timestamp: datetime
    emission_type: str
    payload: Any
    caused_by: str
    schema_version: str = DEFAULT_SCHEMA_VERSION
    trace: TraceContext | None = None
    entity_refs: tuple[EntityRef, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        object.__setattr__(self, "timestamp", ensure_utc(self.timestamp))
