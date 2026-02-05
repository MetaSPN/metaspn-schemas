from __future__ import annotations

from datetime import datetime, timezone

from metaspn_schemas.core import EmissionEnvelope, EntityRef, SchemaVersion, SignalEnvelope, TraceContext
from metaspn_schemas.entities import EntityAliasAdded, EntityMerged, EntityResolved
from metaspn_schemas.features import GameClassified, PlaybookRouted, ProfileEnriched, ScoresComputed
from metaspn_schemas.outcomes import MeetingBooked, MessageSent, ReplyReceived, RevenueEvent
from metaspn_schemas.social import ProfileSnapshotSeen, SocialPostSeen
from metaspn_schemas.state_fragments import Attempts, Cooldowns, Evidence, Identity, Scores
from metaspn_schemas.tasks import Result, Task

NOW = datetime(2026, 1, 1, 12, 0, tzinfo=timezone.utc)


def assert_round_trip(instance: object, cls: type) -> None:
    as_dict = instance.to_dict()
    rebuilt = cls.from_dict(as_dict)
    assert rebuilt == instance


def test_round_trip_core_schemas() -> None:
    entity_ref = EntityRef(ref_type="entity_id", value="ent_1")
    trace = TraceContext(
        trace_id="tr_1",
        caused_by=("s_1",),
        provenance="ingestor",
        redactions=("content",),
        metadata={"a": "1", "b": "2"},
    )
    signal = SignalEnvelope(
        signal_id="s_1",
        timestamp=NOW,
        source="source",
        payload_type="SocialPostSeen",
        payload={"b": 2, "a": 1},
        entity_refs=(entity_ref,),
        trace=trace,
        raw={"secret": "raw"},
    )
    emission = EmissionEnvelope(
        emission_id="e_1",
        timestamp=NOW,
        emission_type="ScoresComputed",
        payload={"score": 0.9},
        caused_by="s_1",
        trace=trace,
        entity_refs=(entity_ref,),
    )

    assert_round_trip(SchemaVersion(), SchemaVersion)
    assert_round_trip(entity_ref, EntityRef)
    assert_round_trip(trace, TraceContext)
    assert_round_trip(signal, SignalEnvelope)
    assert_round_trip(emission, EmissionEnvelope)


def test_round_trip_task_contracts() -> None:
    task = Task(
        task_id="t_1",
        task_type="enrich.profile",
        created_at=NOW,
        priority=1,
        entity_ref=EntityRef(ref_type="email", value="x@example.com"),
        inputs={"x": 1},
        context={"team": "growth"},
    )
    result = Result(
        result_id="r_1",
        task_id="t_1",
        status="ok",
        completed_at=NOW,
        outputs={"done": True},
        errors=(),
    )

    assert_round_trip(task, Task)
    assert_round_trip(result, Result)


def test_round_trip_social_outcomes_entities_features_state_fragments() -> None:
    instances = [
        SocialPostSeen("p1", "linkedin", "@a", "hello", NOW, topics=("b", "a")),
        ProfileSnapshotSeen("pr1", "linkedin", "@a", "A", "Bio", NOW, topics=("x", "c")),
        MessageSent("m1", "email", "x@example.com", NOW),
        ReplyReceived("rp1", "m1", "y@example.com", NOW),
        MeetingBooked("mt1", "x@example.com", NOW, NOW, ("a", "b")),
        RevenueEvent("rev1", 120.5, "USD", NOW, "stripe"),
        EntityResolved("ent1", "resolver", NOW, 0.91),
        EntityMerged("ent1", ("ent2", "ent3"), NOW, "dedupe"),
        EntityAliasAdded("ent1", "acme", "domain", NOW),
        ProfileEnriched("ent1", NOW, "summary", topics=("go", "ai")),
        ScoresComputed("ent1", NOW, {"fit": 0.88}, "v1"),
        PlaybookRouted("t1", NOW, "warm_outbound"),
        GameClassified("ent1", NOW, "six_games", 0.77),
        Identity("ent1", "Acme", ("Acme Inc",)),
        Evidence("ev1", "ent1", "web", NOW, {"domain": "acme.com"}),
        Scores("ent1", {"intent": 0.2}, NOW),
        Cooldowns("ent1", "email", NOW),
        Attempts("ent1", 2, NOW),
    ]
    classes = [
        SocialPostSeen,
        ProfileSnapshotSeen,
        MessageSent,
        ReplyReceived,
        MeetingBooked,
        RevenueEvent,
        EntityResolved,
        EntityMerged,
        EntityAliasAdded,
        ProfileEnriched,
        ScoresComputed,
        PlaybookRouted,
        GameClassified,
        Identity,
        Evidence,
        Scores,
        Cooldowns,
        Attempts,
    ]

    for instance, cls in zip(instances, classes, strict=True):
        assert_round_trip(instance, cls)


def test_datetime_serialization_format_is_utc_iso8601() -> None:
    signal = SignalEnvelope(
        signal_id="s_utc",
        timestamp=NOW,
        source="test",
        payload_type="x",
        payload={},
    )

    data = signal.to_dict()
    assert data["timestamp"] == "2026-01-01T12:00:00Z"


def test_privacy_mode_omits_raw_blob() -> None:
    signal = SignalEnvelope(
        signal_id="s_priv",
        timestamp=NOW,
        source="test",
        payload_type="x",
        payload={},
        raw={"body": "sensitive"},
    )

    data = signal.to_dict(privacy_mode=True)
    assert "raw" not in data


def test_deterministic_dict_key_ordering() -> None:
    signal = SignalEnvelope(
        signal_id="s_ord",
        timestamp=NOW,
        source="test",
        payload_type="x",
        payload={"z": {"b": 2, "a": 1}, "a": 10},
    )

    payload = signal.to_dict()["payload"]
    assert list(payload.keys()) == ["a", "z"]
    assert list(payload["z"].keys()) == ["a", "b"]


def test_topic_lists_are_sorted_on_construction() -> None:
    post = SocialPostSeen("p", "x", "@u", "c", NOW, topics=("ml", "ai"))
    enriched = ProfileEnriched("ent", NOW, "s", topics=("z", "a"))

    assert post.topics == ("ai", "ml")
    assert enriched.topics == ("a", "z")
