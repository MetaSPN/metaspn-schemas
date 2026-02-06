from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from metaspn_schemas.core import DEFAULT_SCHEMA_VERSION
from metaspn_schemas.utils.serde import Serializable
from metaspn_schemas.utils.time import ensure_utc


@dataclass(frozen=True)
class MessageSent(Serializable):
    message_id: str
    channel: str
    recipient: str
    sent_at: datetime
    subject: str | None = None
    schema_version: str = DEFAULT_SCHEMA_VERSION

    def __post_init__(self) -> None:
        object.__setattr__(self, "sent_at", ensure_utc(self.sent_at))


@dataclass(frozen=True)
class ReplyReceived(Serializable):
    reply_id: str
    message_id: str
    sender: str
    received_at: datetime
    sentiment: str | None = None
    schema_version: str = DEFAULT_SCHEMA_VERSION

    def __post_init__(self) -> None:
        object.__setattr__(self, "received_at", ensure_utc(self.received_at))


@dataclass(frozen=True)
class MeetingBooked(Serializable):
    meeting_id: str
    organizer: str
    booked_at: datetime
    starts_at: datetime
    attendees: tuple[str, ...]
    schema_version: str = DEFAULT_SCHEMA_VERSION

    def __post_init__(self) -> None:
        object.__setattr__(self, "booked_at", ensure_utc(self.booked_at))
        object.__setattr__(self, "starts_at", ensure_utc(self.starts_at))


@dataclass(frozen=True)
class RevenueEvent(Serializable):
    revenue_id: str
    amount: float
    currency: str
    recognized_at: datetime
    source: str
    schema_version: str = DEFAULT_SCHEMA_VERSION

    def __post_init__(self) -> None:
        object.__setattr__(self, "recognized_at", ensure_utc(self.recognized_at))


@dataclass(frozen=True)
class NoReplyObserved(Serializable):
    no_reply_id: str
    message_id: str
    observed_at: datetime
    wait_hours: int
    schema_version: str = DEFAULT_SCHEMA_VERSION
    reason: str = "timeout"
    metadata: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "observed_at", ensure_utc(self.observed_at))
