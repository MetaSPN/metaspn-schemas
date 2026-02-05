from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from metaspn_schemas.core import DEFAULT_SCHEMA_VERSION
from metaspn_schemas.utils.serde import Serializable


@dataclass(frozen=True)
class SocialPostSeen(Serializable):
    post_id: str
    platform: str
    author_handle: str
    content: str
    seen_at: datetime
    url: str | None = None
    topics: tuple[str, ...] = field(default_factory=tuple)
    schema_version: str = DEFAULT_SCHEMA_VERSION

    def __post_init__(self) -> None:
        object.__setattr__(self, "topics", tuple(sorted(self.topics)))


@dataclass(frozen=True)
class ProfileSnapshotSeen(Serializable):
    profile_id: str
    platform: str
    handle: str
    display_name: str | None
    bio: str | None
    seen_at: datetime
    followers_count: int | None = None
    topics: tuple[str, ...] = field(default_factory=tuple)
    schema_version: str = DEFAULT_SCHEMA_VERSION

    def __post_init__(self) -> None:
        object.__setattr__(self, "topics", tuple(sorted(self.topics)))
