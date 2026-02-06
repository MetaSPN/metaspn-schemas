from __future__ import annotations

from datetime import datetime, timezone

from metaspn_schemas import ApprovalOverride, DailyDigestEntry, DraftMessage, Recommendation
from metaspn_schemas.core import DEFAULT_SCHEMA_VERSION

NOW = datetime(2026, 2, 6, 15, 0, tzinfo=timezone.utc)


def assert_round_trip(instance: object, cls: type) -> None:
    payload = instance.to_dict()
    rebuilt = cls.from_dict(payload)
    assert rebuilt == instance


def test_round_trip_recommendation_contracts() -> None:
    recommendation = Recommendation(
        recommendation_id="rec_1",
        entity_id="ent_1",
        playbook="warm_outbound",
        score=0.86,
        rationale="Strong fit + quality.",
        priority=1,
        created_at=NOW,
        metadata={"worker": "m2"},
    )
    digest = DailyDigestEntry(
        digest_entry_id="dig_1",
        entity_id="ent_1",
        rank=1,
        action_item="Send intro message",
        created_at=NOW,
        metadata={"source": "daily_digest"},
    )
    draft = DraftMessage(
        draft_id="drf_1",
        entity_id="ent_1",
        channel="email",
        subject="Quick idea for Acme",
        body="Would love to share a short idea...",
        tone="professional",
        constraints=("no_links", "under_120_words"),
        created_at=NOW,
    )
    approval = ApprovalOverride(
        approval_id="apr_1",
        draft_id="drf_1",
        status="approved",
        reason="Looks good",
        reviewed_at=NOW,
        reviewer="ops@metaspn",
    )

    assert_round_trip(recommendation, Recommendation)
    assert_round_trip(digest, DailyDigestEntry)
    assert_round_trip(draft, DraftMessage)
    assert_round_trip(approval, ApprovalOverride)


def test_m2_deterministic_serialization_and_defaults() -> None:
    recommendation = Recommendation(
        recommendation_id="rec_1",
        entity_id="ent_1",
        playbook="warm_outbound",
        score=0.86,
        rationale="Strong fit + quality.",
        priority=1,
        created_at=NOW,
        metadata={"z": "2", "a": "1"},
    )
    draft = DraftMessage(
        draft_id="drf_1",
        entity_id="ent_1",
        channel="email",
        body="hello",
        tone="professional",
        created_at=NOW,
        constraints=("z", "a"),
    )

    rec_data = recommendation.to_dict()
    draft_data = draft.to_dict()

    assert rec_data["schema_version"] == DEFAULT_SCHEMA_VERSION
    assert list(rec_data["metadata"].keys()) == ["a", "z"]
    assert draft_data["constraints"] == ["a", "z"]
    assert draft_data["created_at"] == "2026-02-06T15:00:00Z"
