from __future__ import annotations

from datetime import datetime, timezone

from metaspn_schemas.core import DEFAULT_SCHEMA_VERSION, EntityRef
from metaspn_schemas.ingestion import (
    IngestionParseErrorEvent,
    NormalizedSocialPostSeenEvent,
    RawSocialPostSeenEvent,
    ResolverHandoff,
)

NOW = datetime(2026, 2, 6, 12, 0, tzinfo=timezone.utc)


def assert_round_trip(instance: object, cls: type) -> None:
    data = instance.to_dict()
    rebuilt = cls.from_dict(data)
    assert rebuilt == instance


def test_round_trip_ingestion_contracts() -> None:
    handoff = ResolverHandoff(
        handoff_id="rh_1",
        entity_ref=EntityRef(ref_type="email", value="x@example.com"),
        provenance_source="linkedin.webhook",
        provenance_step="ingestion.normalize",
        attached_at=NOW,
        metadata={"worker": "m0"},
    )

    raw_event = RawSocialPostSeenEvent(
        event_id="raw_1",
        source="linkedin.webhook",
        seen_at=NOW,
        raw={"id": "p1", "text": "hello"},
        resolver_handoff=handoff,
    )
    normalized_event = NormalizedSocialPostSeenEvent(
        event_id="norm_1",
        source="linkedin.webhook",
        platform="linkedin",
        post_id="p1",
        author_handle="@a",
        content="hello",
        seen_at=NOW,
        topics=("b", "a"),
        resolver_handoff=handoff,
    )
    parse_error = IngestionParseErrorEvent(
        error_id="err_1",
        source="linkedin.webhook",
        occurred_at=NOW,
        error_type="parse_error",
        message="missing content field",
        raw_payload={"id": "p1"},
        resolver_handoff=handoff,
    )

    assert_round_trip(handoff, ResolverHandoff)
    assert_round_trip(raw_event, RawSocialPostSeenEvent)
    assert_round_trip(normalized_event, NormalizedSocialPostSeenEvent)
    assert_round_trip(parse_error, IngestionParseErrorEvent)


def test_ingestion_schema_version_defaults() -> None:
    raw_event = RawSocialPostSeenEvent(
        event_id="raw_1",
        source="linkedin.webhook",
        seen_at=NOW,
        raw={"id": "p1"},
    )

    assert raw_event.schema_version == DEFAULT_SCHEMA_VERSION


def test_ingestion_topics_sorted_and_timestamps_utc() -> None:
    event = NormalizedSocialPostSeenEvent(
        event_id="norm_1",
        source="linkedin.webhook",
        platform="linkedin",
        post_id="p1",
        author_handle="@a",
        content="hello",
        seen_at=NOW,
        topics=("z", "a"),
    )

    assert event.topics == ("a", "z")
    assert event.to_dict()["seen_at"] == "2026-02-06T12:00:00Z"
