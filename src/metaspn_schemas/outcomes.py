from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from metaspn_schemas.core import DEFAULT_SCHEMA_VERSION
from metaspn_schemas.utils.serde import Serializable


@dataclass(frozen=True)
class MessageSent(Serializable):
    message_id: str
    channel: str
    recipient: str
    sent_at: datetime
    subject: str | None = None
    schema_version: str = DEFAULT_SCHEMA_VERSION


@dataclass(frozen=True)
class ReplyReceived(Serializable):
    reply_id: str
    message_id: str
    sender: str
    received_at: datetime
    sentiment: str | None = None
    schema_version: str = DEFAULT_SCHEMA_VERSION


@dataclass(frozen=True)
class MeetingBooked(Serializable):
    meeting_id: str
    organizer: str
    booked_at: datetime
    starts_at: datetime
    attendees: tuple[str, ...]
    schema_version: str = DEFAULT_SCHEMA_VERSION


@dataclass(frozen=True)
class RevenueEvent(Serializable):
    revenue_id: str
    amount: float
    currency: str
    recognized_at: datetime
    source: str
    schema_version: str = DEFAULT_SCHEMA_VERSION
